import asyncio
from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import session_factory
from app.models import (
    Activity,
    Building,
    Contract,
    ContractParty,
    Delay,
    Factory,
    Invoice,
    Manufacturer,
    Material,
    Milestone,
    Payment,
    Project,
    Risk,
    Schedule,
    ScheduleVersion,
    Site,
    Subcontract,
    Supplier,
)
from app.models.identity import Organization


async def seed_development_data(session: AsyncSession) -> Organization:
    existing = await session.scalar(select(Organization).where(Organization.code == "CONTRACTOR-X"))
    if existing is not None:
        return existing

    tenant = Organization(name="Contractor X", code="CONTRACTOR-X")
    session.add(tenant)
    await session.flush()
    tenant_id = tenant.id

    subcontractor = Supplier(tenant_id=tenant_id, name="Subcontractor Y", code="SUBCONTRACTOR-Y")
    supplier = Supplier(tenant_id=tenant_id, name="Supplier Z", code="SUPPLIER-Z")
    project = Project(tenant_id=tenant_id, name="Project A", code="PROJECT-A")
    session.add_all([subcontractor, supplier, project])
    await session.flush()

    manufacturer = Manufacturer(
        tenant_id=tenant_id, supplier_id=supplier.id, name="Manufacturer F", code="MFG-F"
    )
    site = Site(tenant_id=tenant_id, project_id=project.id, name="Project A Site", code="SITE-A")
    schedule = Schedule(
        tenant_id=tenant_id, project_id=project.id, name="Project A Master Schedule"
    )
    contract = Contract(
        tenant_id=tenant_id,
        project_id=project.id,
        number="C234",
        title="Project A Main Contract",
        contract_type="main",
        value=Decimal("10000000"),
    )
    session.add_all([manufacturer, site, schedule, contract])
    await session.flush()

    factory = Factory(
        tenant_id=tenant_id,
        manufacturer_id=manufacturer.id,
        name="Factory F3",
        code="F3",
    )
    material = Material(
        tenant_id=tenant_id,
        manufacturer_id=manufacturer.id,
        name="Material M42",
        code="M42",
        unit="tonne",
    )
    building = Building(tenant_id=tenant_id, site_id=site.id, name="Building B", code="BUILDING-B")
    version = ScheduleVersion(
        tenant_id=tenant_id,
        schedule_id=schedule.id,
        version_number=1,
        data_date=date.today(),
    )
    session.add_all([factory, material, building, version])
    await session.flush()

    activity = Activity(
        tenant_id=tenant_id,
        schedule_version_id=version.id,
        name="Activity A45",
        code="A45",
        planned_start=datetime.now(UTC),
        percent_complete=Decimal("0"),
    )
    risk = Risk(
        tenant_id=tenant_id,
        project_id=project.id,
        code="R17",
        title="Risk R17",
        probability=Decimal("25"),
        impact=Decimal("500000"),
    )
    invoice = Invoice(
        tenant_id=tenant_id,
        contract_id=contract.id,
        supplier_id=supplier.id,
        number="I993",
        amount=Decimal("250000"),
        invoice_date=date.today(),
    )
    session.add_all([activity, risk, invoice])
    await session.flush()

    session.add_all(
        [
            Milestone(
                tenant_id=tenant_id,
                schedule_version_id=version.id,
                activity_id=activity.id,
                name="Milestone M17",
                code="M17",
            ),
            Delay(
                tenant_id=tenant_id,
                project_id=project.id,
                activity_id=activity.id,
                code="D5",
                title="Delay D5",
                delay_days=Decimal("5"),
            ),
            ContractParty(
                tenant_id=tenant_id,
                contract_id=contract.id,
                organization_id=tenant.id,
                name="Contractor X",
                party_type="contractor",
            ),
            Subcontract(
                tenant_id=tenant_id,
                contract_id=contract.id,
                subcontractor_id=subcontractor.id,
                number="SC-Y",
                title="Subcontractor Y Works",
                value=Decimal("1000000"),
            ),
            Payment(
                tenant_id=tenant_id,
                invoice_id=invoice.id,
                reference="P883",
                amount=Decimal("250000"),
                payment_date=date.today(),
            ),
        ]
    )
    await session.commit()
    return tenant


async def main() -> None:
    async with session_factory() as session:
        tenant = await seed_development_data(session)
        print(f"Development data ready for tenant {tenant.id}")


if __name__ == "__main__":
    asyncio.run(main())
