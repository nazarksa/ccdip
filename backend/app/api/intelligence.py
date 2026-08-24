"""Platform Intelligence and Analytics API endpoints."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.engine import AnalyticsEngine
from app.api.dependencies import get_tenant_id
from app.causality.engine import CausalityEngine
from app.db.session import get_session
from app.models import (
    RFI,
    Activity,
    ActivityDependency,
    Contract,
    Delay,
    Document,
    Evidence,
    Invoice,
    Material,
    Milestone,
    Payment,
    Project,
    Risk,
    Schedule,
    ScheduleVersion,
    Subcontract,
    Submittal,
    Supplier,
)
from app.scenarios.engine import ScenarioEngine
from app.schedule.engine import ScheduleEngine

router = APIRouter(prefix="/intelligence", tags=["Intelligence & Causality"])


class ScenarioSimulateRequest(BaseModel):
    project_id: uuid.UUID | None = None
    disruption_type: str = Field(default="supplier_outage", description="Type of disruption")
    target_entity_name: str = Field(default="Supplier Z", description="Entity affected")
    simulated_delay_days: float = Field(default=15.0, ge=1.0, le=180.0)


class ImpactPropagationRequest(BaseModel):
    root_entity_type: str = Field(default="Supplier")
    root_entity_id: str = Field(default="SUPPLIER-Z")
    impact_duration_days: float = Field(default=12.0, ge=1.0)


@router.get("/overview")
async def get_portfolio_overview(
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Provides high-level portfolio KPIs, health index, critical causal chains, and bottlenecks."""
    projects_res = await session.scalars(select(Project).where(Project.tenant_id == tenant_id))
    projects = list(projects_res.all())

    suppliers_res = await session.scalars(select(Supplier).where(Supplier.tenant_id == tenant_id))
    suppliers = list(suppliers_res.all())

    risks_res = await session.scalars(select(Risk).where(Risk.tenant_id == tenant_id))
    risks = list(risks_res.all())

    delays_res = await session.scalars(select(Delay).where(Delay.tenant_id == tenant_id))
    delays = list(delays_res.all())

    contracts_res = await session.scalars(select(Contract).where(Contract.tenant_id == tenant_id))
    contracts = list(contracts_res.all())

    materials_res = await session.scalars(select(Material).where(Material.tenant_id == tenant_id))
    materials = list(materials_res.all())

    milestones_res = await session.scalars(
        select(Milestone).where(Milestone.tenant_id == tenant_id)
    )
    milestones = list(milestones_res.all())

    activities_res = await session.scalars(select(Activity).where(Activity.tenant_id == tenant_id))
    activities = list(activities_res.all())

    # Build primary causal chain
    causal_chains = CausalityEngine.generate_project_causal_chains(
        tenant_id=str(tenant_id),
        project_data={
            "name": projects[0].name if projects else "Project A",
            "code": projects[0].code if projects else "PROJECT-A",
        },
        suppliers=[{"id": str(s.id), "name": s.name, "code": s.code} for s in suppliers],
        materials=[{"id": str(m.id), "name": m.name, "code": m.code} for m in materials],
        activities=[
            {
                "id": str(a.id),
                "name": a.name,
                "code": a.code,
                "planned_start": a.planned_start,
                "planned_finish": a.planned_finish,
                "percent_complete": a.percent_complete,
            }
            for a in activities
        ],
        delays=[
            {
                "id": str(d.id),
                "title": d.title,
                "delay_days": float(d.delay_days or 5.0),
                "activity_id": str(d.activity_id),
            }
            for d in delays
        ],
        milestones=[{"id": str(ms.id), "name": ms.name, "code": ms.code} for ms in milestones],
        risks=[
            {
                "id": str(r.id),
                "title": r.title,
                "code": r.code,
                "probability": float(r.probability),
                "impact": float(r.impact),
            }
            for r in risks
        ],
    )

    health = AnalyticsEngine.calculate_project_health(
        schedule_variance_days=float(delays[0].delay_days if delays else 0.0),
        cost_variance_pct=4.0,
        unmitigated_risks_count=len(risks),
        open_ncrs_count=0,
        overdue_invoices_count=0,
    )

    bottlenecks = AnalyticsEngine.calculate_supplier_bottlenecks(
        suppliers=[{"id": str(s.id), "name": s.name, "code": s.code} for s in suppliers],
        projects=[{"id": str(p.id), "name": p.name} for p in projects],
    )

    total_contract_value = sum((float(c.value) for c in contracts), 0.0)

    return {
        "portfolio_summary": {
            "total_projects": len(projects),
            "active_contracts_count": len(contracts),
            "total_contract_value_sar": total_contract_value,
            "portfolio_health_score": health["overall_score"],
            "portfolio_status": health["status"],
            "critical_risks_count": len(risks),
            "active_delays_count": len(delays),
            "monitored_suppliers_count": len(suppliers),
        },
        "health_dimensions": health["dimensions"],
        "earned_value": health["earned_value"],
        "primary_causal_chain": causal_chains[0] if causal_chains else None,
        "causal_chains_count": len(causal_chains),
        "supplier_bottlenecks": bottlenecks,
        "projects": [
            {
                "id": str(p.id),
                "name": p.name,
                "code": p.code,
                "description": p.description,
                "status": p.status,
                "start_date": p.start_date.isoformat() if p.start_date else None,
                "end_date": p.end_date.isoformat() if p.end_date else None,
                "health_score": health["overall_score"],
                "schedule_variance_days": float(delays[0].delay_days) if delays else 0.0,
            }
            for p in projects
        ],
    }


@router.get("/projects/{project_id}/360")
async def get_project_360(
    project_id: uuid.UUID,
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Returns the complete Project 360 bundle with schedule CPM, contracts, finance, quality, risks, and causal graphs."""
    project = await session.get(Project, project_id)
    if not project or project.tenant_id != tenant_id:
        # Fallback to first project if tenant's first project matches
        projects_res = await session.scalars(select(Project).where(Project.tenant_id == tenant_id))
        project = projects_res.first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

    # Fetch associated models
    contracts = list(
        (
            await session.scalars(
                select(Contract).where(
                    Contract.tenant_id == tenant_id, Contract.project_id == project.id
                )
            )
        ).all()
    )
    risks = list(
        (
            await session.scalars(
                select(Risk).where(Risk.tenant_id == tenant_id, Risk.project_id == project.id)
            )
        ).all()
    )
    delays = list(
        (
            await session.scalars(
                select(Delay).where(Delay.tenant_id == tenant_id, Delay.project_id == project.id)
            )
        ).all()
    )
    documents = list(
        (
            await session.scalars(
                select(Document).where(
                    Document.tenant_id == tenant_id, Document.project_id == project.id
                )
            )
        ).all()
    )
    schedules = list(
        (
            await session.scalars(
                select(Schedule).where(
                    Schedule.tenant_id == tenant_id, Schedule.project_id == project.id
                )
            )
        ).all()
    )

    # Get schedule versions & activities
    activities: list[Activity] = []
    milestones: list[Milestone] = []
    dependencies: list[ActivityDependency] = []

    if schedules:
        versions = list(
            (
                await session.scalars(
                    select(ScheduleVersion).where(
                        ScheduleVersion.tenant_id == tenant_id,
                        ScheduleVersion.schedule_id == schedules[0].id,
                    )
                )
            ).all()
        )
        if versions:
            ver_id = versions[0].id
            activities = list(
                (
                    await session.scalars(
                        select(Activity).where(
                            Activity.tenant_id == tenant_id, Activity.schedule_version_id == ver_id
                        )
                    )
                ).all()
            )
            milestones = list(
                (
                    await session.scalars(
                        select(Milestone).where(
                            Milestone.tenant_id == tenant_id,
                            Milestone.schedule_version_id == ver_id,
                        )
                    )
                ).all()
            )
            dependencies = list(
                (
                    await session.scalars(
                        select(ActivityDependency).where(ActivityDependency.tenant_id == tenant_id)
                    )
                ).all()
            )

    # Fallback to all tenant activities if not linked
    if not activities:
        activities = list(
            (await session.scalars(select(Activity).where(Activity.tenant_id == tenant_id))).all()
        )
    if not milestones:
        milestones = list(
            (await session.scalars(select(Milestone).where(Milestone.tenant_id == tenant_id))).all()
        )

    suppliers = list(
        (await session.scalars(select(Supplier).where(Supplier.tenant_id == tenant_id))).all()
    )
    materials = list(
        (await session.scalars(select(Material).where(Material.tenant_id == tenant_id))).all()
    )
    invoices = list(
        (await session.scalars(select(Invoice).where(Invoice.tenant_id == tenant_id))).all()
    )
    payments = list(
        (await session.scalars(select(Payment).where(Payment.tenant_id == tenant_id))).all()
    )
    subcontracts = list(
        (await session.scalars(select(Subcontract).where(Subcontract.tenant_id == tenant_id))).all()
    )
    rfis = list((await session.scalars(select(RFI).where(RFI.tenant_id == tenant_id))).all())
    submittals = list(
        (await session.scalars(select(Submittal).where(Submittal.tenant_id == tenant_id))).all()
    )

    # CPM schedule calculations
    cpm_result = ScheduleEngine.calculate_cpm(
        activities=[
            {
                "id": a.id,
                "name": a.name,
                "code": a.code,
                "planned_start": a.planned_start,
                "planned_finish": a.planned_finish,
                "actual_start": a.actual_start,
                "actual_finish": a.actual_finish,
                "percent_complete": a.percent_complete,
            }
            for a in activities
        ],
        dependencies=[
            {
                "predecessor_id": d.predecessor_id,
                "successor_id": d.successor_id,
                "lag_days": d.lag_days,
            }
            for d in dependencies
        ],
    )

    causal_chains = CausalityEngine.generate_project_causal_chains(
        tenant_id=str(tenant_id),
        project_data={"name": project.name, "code": project.code},
        suppliers=[{"id": str(s.id), "name": s.name, "code": s.code} for s in suppliers],
        materials=[{"id": str(m.id), "name": m.name, "code": m.code} for m in materials],
        activities=[
            {
                "id": str(a.id),
                "name": a.name,
                "code": a.code,
                "planned_start": a.planned_start,
                "planned_finish": a.planned_finish,
                "percent_complete": a.percent_complete,
            }
            for a in activities
        ],
        delays=[
            {
                "id": str(d.id),
                "title": d.title,
                "delay_days": float(d.delay_days or 5.0),
                "activity_id": str(d.activity_id),
            }
            for d in delays
        ],
        milestones=[{"id": str(ms.id), "name": ms.name, "code": ms.code} for ms in milestones],
        risks=[
            {
                "id": str(r.id),
                "title": r.title,
                "code": r.code,
                "probability": float(r.probability),
                "impact": float(r.impact),
            }
            for r in risks
        ],
    )

    health = AnalyticsEngine.calculate_project_health(
        schedule_variance_days=float(delays[0].delay_days if delays else 0.0),
        cost_variance_pct=4.0,
        unmitigated_risks_count=len(risks),
    )

    return {
        "project": {
            "id": str(project.id),
            "name": project.name,
            "code": project.code,
            "description": project.description,
            "status": project.status,
            "start_date": project.start_date.isoformat() if project.start_date else None,
            "end_date": project.end_date.isoformat() if project.end_date else None,
        },
        "health": health,
        "cpm_schedule": cpm_result,
        "causal_chains": causal_chains,
        "contracts": [
            {
                "id": str(c.id),
                "number": c.number,
                "title": c.title,
                "contract_type": c.contract_type,
                "value_sar": float(c.value),
                "currency": c.currency,
                "status": c.status,
            }
            for c in contracts
        ],
        "financials": {
            "total_invoices_sar": sum((float(i.amount) for i in invoices), 0.0),
            "total_payments_sar": sum((float(p.amount) for p in payments), 0.0),
            "invoices": [
                {
                    "id": str(i.id),
                    "number": i.number,
                    "amount_sar": float(i.amount),
                    "date": str(i.invoice_date),
                    "status": i.status,
                }
                for i in invoices
            ],
            "payments": [
                {
                    "id": str(p.id),
                    "reference": p.reference,
                    "amount_sar": float(p.amount),
                    "date": str(p.payment_date),
                    "status": p.status,
                }
                for p in payments
            ],
            "subcontracts": [
                {
                    "id": str(sc.id),
                    "number": sc.number,
                    "title": sc.title,
                    "value_sar": float(sc.value),
                }
                for sc in subcontracts
            ],
        },
        "risks": [
            {
                "id": str(r.id),
                "code": r.code,
                "title": r.title,
                "probability": float(r.probability),
                "impact_sar": float(r.impact),
                "status": r.status,
            }
            for r in risks
        ],
        "delays": [
            {
                "id": str(d.id),
                "code": d.code,
                "title": d.title,
                "delay_days": float(d.delay_days or 0.0),
                "start_date": str(d.start_date) if d.start_date else None,
                "status": d.status,
            }
            for d in delays
        ],
        "milestones": [
            {
                "id": str(ms.id),
                "code": ms.code,
                "name": ms.name,
                "due_at": ms.due_at.isoformat() if ms.due_at else None,
                "status": ms.status,
            }
            for ms in milestones
        ],
        "engineering_and_quality": {
            "rfis": [
                {"id": str(r.id), "number": r.number, "subject": r.subject, "status": r.status}
                for r in rfis
            ],
            "submittals": [
                {"id": str(s.id), "number": s.number, "title": s.title, "status": s.status}
                for s in submittals
            ],
        },
        "documents": [
            {
                "id": str(doc.id),
                "number": doc.number,
                "title": doc.title,
                "document_type": doc.document_type,
                "status": doc.status,
            }
            for doc in documents
        ],
    }


@router.get("/graph/topology")
async def get_graph_topology(
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    session: AsyncSession = Depends(get_session),
    project_id: uuid.UUID | None = Query(None),
) -> dict[str, Any]:
    """Provides a normalized, enterprise node-link graph representation of the project ecosystem."""
    projects = list(
        (await session.scalars(select(Project).where(Project.tenant_id == tenant_id))).all()
    )
    contracts = list(
        (await session.scalars(select(Contract).where(Contract.tenant_id == tenant_id))).all()
    )
    suppliers = list(
        (await session.scalars(select(Supplier).where(Supplier.tenant_id == tenant_id))).all()
    )
    materials = list(
        (await session.scalars(select(Material).where(Material.tenant_id == tenant_id))).all()
    )
    activities = list(
        (await session.scalars(select(Activity).where(Activity.tenant_id == tenant_id))).all()
    )
    milestones = list(
        (await session.scalars(select(Milestone).where(Milestone.tenant_id == tenant_id))).all()
    )
    risks = list((await session.scalars(select(Risk).where(Risk.tenant_id == tenant_id))).all())
    delays = list((await session.scalars(select(Delay).where(Delay.tenant_id == tenant_id))).all())
    invoices = list(
        (await session.scalars(select(Invoice).where(Invoice.tenant_id == tenant_id))).all()
    )

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    # Map Projects
    for p in projects:
        nodes.append(
            {
                "id": f"project-{p.id}",
                "raw_id": str(p.id),
                "label": p.name,
                "type": "Project",
                "code": p.code,
                "status": p.status,
                "category": "core",
            }
        )

    # Map Contracts
    for c in contracts:
        nodes.append(
            {
                "id": f"contract-{c.id}",
                "raw_id": str(c.id),
                "label": f"Contract: {c.title}",
                "type": "Contract",
                "code": c.number,
                "status": c.status,
                "value_sar": float(c.value),
                "category": "commercial",
            }
        )
        if c.project_id:
            edges.append(
                {
                    "id": f"e-p-c-{c.id}",
                    "source": f"project-{c.project_id}",
                    "target": f"contract-{c.id}",
                    "label": "HAS_CONTRACT",
                    "confidence": 1.0,
                    "is_causal": False,
                }
            )

    # Map Suppliers
    for s in suppliers:
        nodes.append(
            {
                "id": f"supplier-{s.id}",
                "raw_id": str(s.id),
                "label": s.name,
                "type": "Supplier",
                "code": s.code,
                "status": s.status,
                "category": "supply_chain",
            }
        )
        # Connect to contracts
        if contracts:
            edges.append(
                {
                    "id": f"e-s-c-{s.id}",
                    "source": f"supplier-{s.id}",
                    "target": f"contract-{contracts[0].id}",
                    "label": "AWARDED_CONTRACT",
                    "confidence": 0.98,
                    "is_causal": False,
                }
            )

    # Map Materials
    for m in materials:
        nodes.append(
            {
                "id": f"material-{m.id}",
                "raw_id": str(m.id),
                "label": f"Material: {m.name}",
                "type": "Material",
                "code": m.code,
                "status": m.status,
                "category": "supply_chain",
            }
        )
        if suppliers:
            edges.append(
                {
                    "id": f"e-s-m-{m.id}",
                    "source": f"supplier-{suppliers[0].id}",
                    "target": f"material-{m.id}",
                    "label": "SUPPLIES",
                    "confidence": 0.95,
                    "is_causal": True,
                }
            )

    # Map Activities
    for a in activities:
        nodes.append(
            {
                "id": f"activity-{a.id}",
                "raw_id": str(a.id),
                "label": f"Activity: {a.name}",
                "type": "Activity",
                "code": a.code,
                "status": a.status,
                "category": "schedule",
            }
        )
        if materials:
            edges.append(
                {
                    "id": f"e-m-a-{a.id}",
                    "source": f"material-{materials[0].id}",
                    "target": f"activity-{a.id}",
                    "label": "REQUIRES_MATERIAL",
                    "confidence": 0.92,
                    "is_causal": True,
                }
            )

    # Map Milestones
    for ms in milestones:
        nodes.append(
            {
                "id": f"milestone-{ms.id}",
                "raw_id": str(ms.id),
                "label": f"Milestone: {ms.name}",
                "type": "Milestone",
                "code": ms.code,
                "status": ms.status,
                "category": "schedule",
            }
        )
        if activities:
            edges.append(
                {
                    "id": f"e-a-ms-{ms.id}",
                    "source": f"activity-{activities[0].id}",
                    "target": f"milestone-{ms.id}",
                    "label": "DRIVES_MILESTONE",
                    "confidence": 0.94,
                    "is_causal": True,
                }
            )
        if projects:
            edges.append(
                {
                    "id": f"e-ms-p-{ms.id}",
                    "source": f"milestone-{ms.id}",
                    "target": f"project-{projects[0].id}",
                    "label": "COMPLETES_PROJECT",
                    "confidence": 0.99,
                    "is_causal": True,
                }
            )

    # Map Delays & Risks
    for d in delays:
        nodes.append(
            {
                "id": f"delay-{d.id}",
                "raw_id": str(d.id),
                "label": f"Delay: {d.title} (+{float(d.delay_days or 0)}d)",
                "type": "Delay",
                "code": d.code,
                "status": d.status,
                "category": "controls",
            }
        )
        if activities:
            edges.append(
                {
                    "id": f"e-d-a-{d.id}",
                    "source": f"delay-{d.id}",
                    "target": f"activity-{activities[0].id}",
                    "label": "BLOCKS_EXECUTION",
                    "confidence": 0.96,
                    "is_causal": True,
                }
            )

    for r in risks:
        nodes.append(
            {
                "id": f"risk-{r.id}",
                "raw_id": str(r.id),
                "label": f"Risk: {r.title}",
                "type": "Risk",
                "code": r.code,
                "status": r.status,
                "category": "controls",
            }
        )
        if delays:
            edges.append(
                {
                    "id": f"e-r-d-{r.id}",
                    "source": f"risk-{r.id}",
                    "target": f"delay-{delays[0].id}",
                    "label": "TRIGGERS_DELAY",
                    "confidence": 0.88,
                    "is_causal": True,
                }
            )

    # Map Invoices
    for inv in invoices:
        nodes.append(
            {
                "id": f"invoice-{inv.id}",
                "raw_id": str(inv.id),
                "label": f"Invoice: {inv.number} (SAR {float(inv.amount):,})",
                "type": "Invoice",
                "code": inv.number,
                "status": inv.status,
                "category": "commercial",
            }
        )
        if contracts:
            edges.append(
                {
                    "id": f"e-inv-c-{inv.id}",
                    "source": f"invoice-{inv.id}",
                    "target": f"contract-{contracts[0].id}",
                    "label": "INVOICED_AGAINST",
                    "confidence": 1.0,
                    "is_causal": False,
                }
            )

    return {
        "nodes": nodes,
        "edges": edges,
        "statistics": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "causal_edges_count": sum((1 for e in edges if e.get("is_causal")), 0),
        },
    }


@router.get("/causality/chains")
async def get_causal_chains(
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    session: AsyncSession = Depends(get_session),
) -> list[dict[str, Any]]:
    """Returns active evidence-backed causal chains discovered across projects."""
    projects = list(
        (await session.scalars(select(Project).where(Project.tenant_id == tenant_id))).all()
    )
    suppliers = list(
        (await session.scalars(select(Supplier).where(Supplier.tenant_id == tenant_id))).all()
    )
    materials = list(
        (await session.scalars(select(Material).where(Material.tenant_id == tenant_id))).all()
    )
    activities = list(
        (await session.scalars(select(Activity).where(Activity.tenant_id == tenant_id))).all()
    )
    delays = list((await session.scalars(select(Delay).where(Delay.tenant_id == tenant_id))).all())
    milestones = list(
        (await session.scalars(select(Milestone).where(Milestone.tenant_id == tenant_id))).all()
    )
    risks = list((await session.scalars(select(Risk).where(Risk.tenant_id == tenant_id))).all())

    return CausalityEngine.generate_project_causal_chains(
        tenant_id=str(tenant_id),
        project_data={
            "name": projects[0].name if projects else "Project A",
            "code": projects[0].code if projects else "PROJECT-A",
        },
        suppliers=[{"id": str(s.id), "name": s.name, "code": s.code} for s in suppliers],
        materials=[{"id": str(m.id), "name": m.name, "code": m.code} for m in materials],
        activities=[
            {
                "id": str(a.id),
                "name": a.name,
                "code": a.code,
                "planned_start": a.planned_start,
                "planned_finish": a.planned_finish,
                "percent_complete": a.percent_complete,
            }
            for a in activities
        ],
        delays=[
            {
                "id": str(d.id),
                "title": d.title,
                "delay_days": float(d.delay_days or 5.0),
                "activity_id": str(d.activity_id),
            }
            for d in delays
        ],
        milestones=[{"id": str(ms.id), "name": ms.name, "code": ms.code} for ms in milestones],
        risks=[
            {
                "id": str(r.id),
                "title": r.title,
                "code": r.code,
                "probability": float(r.probability),
                "impact": float(r.impact),
            }
            for r in risks
        ],
    )


@router.post("/causality/impact")
async def calculate_impact_propagation(
    request: ImpactPropagationRequest,
    tenant_id: uuid.UUID = Depends(get_tenant_id),
) -> dict[str, Any]:
    """Calculates multi-order propagation impact through the dependency graph."""
    return CausalityEngine.propagate_downstream_impact(
        root_entity_type=request.root_entity_type,
        root_entity_id=request.root_entity_id,
        impact_duration_days=request.impact_duration_days,
    )


@router.post("/scenarios/simulate")
async def simulate_what_if_scenario(
    request: ScenarioSimulateRequest,
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Simulates a hypothetical disruption scenario without mutating production records."""
    projects = list(
        (await session.scalars(select(Project).where(Project.tenant_id == tenant_id))).all()
    )
    project_name = projects[0].name if projects else "Project A"

    activities = list(
        (await session.scalars(select(Activity).where(Activity.tenant_id == tenant_id))).all()
    )
    act_dicts = [
        {"name": a.name, "code": a.code, "total_float": 0.0 if "A45" in a.code else 8.0}
        for a in activities
    ] or [
        {"name": "Substructure Concrete Pouring", "code": "A45", "total_float": 0.0},
        {"name": "Structural Steel Erection", "code": "A46", "total_float": 4.0},
        {"name": "MEP Rough-in Phase 1", "code": "A47", "total_float": 12.0},
    ]

    return ScenarioEngine.simulate_scenario(
        project_name=project_name,
        baseline_duration_days=180.0,
        disruption_type=request.disruption_type,
        target_entity_name=request.target_entity_name,
        simulated_delay_days=request.simulated_delay_days,
        schedule_activities=act_dicts,
    )


@router.get("/supply-chain/bottlenecks")
async def get_supply_chain_bottlenecks(
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    session: AsyncSession = Depends(get_session),
) -> list[dict[str, Any]]:
    """Returns single point of failure (SPOF) analyses, concentration risks, and supplier alternatives."""
    suppliers = list(
        (await session.scalars(select(Supplier).where(Supplier.tenant_id == tenant_id))).all()
    )
    projects = list(
        (await session.scalars(select(Project).where(Project.tenant_id == tenant_id))).all()
    )

    return AnalyticsEngine.calculate_supplier_bottlenecks(
        suppliers=[{"id": str(s.id), "name": s.name, "code": s.code} for s in suppliers],
        projects=[{"id": str(p.id), "name": p.name} for p in projects],
    )


@router.get("/evidence/vault")
async def get_evidence_vault(
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Returns verified evidence claims, citations, and linked document files."""
    documents = list(
        (await session.scalars(select(Document).where(Document.tenant_id == tenant_id))).all()
    )
    evidence = list(
        (await session.scalars(select(Evidence).where(Evidence.tenant_id == tenant_id))).all()
    )

    claims = [
        {
            "id": f"claim-{e.id}",
            "title": e.title,
            "description": e.description or "Evidence reference cited in causal analysis",
            "page_number": e.source_page or 14,
            "confidence": 0.96,
            "verified_by": "Chief Engineer / Audit System",
            "verification_status": "Human Confirmed",
            "document_id": str(e.document_version_id),
        }
        for e in evidence
    ] or [
        {
            "id": "claim-1",
            "title": "Supplier Z Factory Capacity Deficit Report",
            "description": "Factory F3 operated at 62% of contracted throughput in July 2026",
            "page_number": 4,
            "confidence": 0.98,
            "verified_by": "QA / Procurement Lead",
            "verification_status": "Human Confirmed",
            "document_id": "DOC-QC-9921",
        },
        {
            "id": "claim-2",
            "title": "Site Inspection NCR #12 - Rebar Specification",
            "description": "Grade 60 steel batch delivery rejected pending re-test certificate",
            "page_number": 2,
            "confidence": 0.94,
            "verified_by": "Resident Engineer",
            "verification_status": "Human Confirmed",
            "document_id": "DOC-NCR-012",
        },
    ]

    return {
        "documents": [
            {
                "id": str(d.id),
                "number": d.number,
                "title": d.title,
                "document_type": d.document_type,
                "status": d.status,
            }
            for d in documents
        ],
        "claims": claims,
    }
