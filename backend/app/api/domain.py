from fastapi import APIRouter

from app.api.crud import create_crud_router
from app.models import (
    NCR,
    RFI,
    Activity,
    Contract,
    Delay,
    Document,
    Evidence,
    Inspection,
    Invoice,
    Material,
    Milestone,
    Payment,
    Program,
    Project,
    PurchaseOrder,
    QualityEvent,
    Risk,
    Subcontract,
    Submittal,
    Supplier,
)
from app.schemas.domain import SCHEMAS

router = APIRouter()

for path, tag, model in (
    ("projects", "Projects", Project),
    ("programs", "Programs", Program),
    ("activities", "Activities", Activity),
    ("milestones", "Milestones", Milestone),
    ("suppliers", "Suppliers", Supplier),
    ("materials", "Materials", Material),
    ("contracts", "Contracts", Contract),
    ("subcontracts", "Subcontracts", Subcontract),
    ("purchase-orders", "PurchaseOrders", PurchaseOrder),
    ("invoices", "Invoices", Invoice),
    ("payments", "Payments", Payment),
    ("risks", "Risks", Risk),
    ("delays", "Delays", Delay),
    ("rfis", "RFIs", RFI),
    ("submittals", "Submittals", Submittal),
    ("inspections", "Inspections", Inspection),
    ("ncrs", "NCRs", NCR),
    ("quality-events", "QualityEvents", QualityEvent),
    ("documents", "Documents", Document),
    ("evidence", "Evidence", Evidence),
):
    create_schema, update_schema, read_schema = SCHEMAS[model.__name__]
    router.include_router(
        create_crud_router(
            path=path,
            tag=tag,
            model=model,
            create_schema=create_schema,
            update_schema=update_schema,
            read_schema=read_schema,
        )
    )
