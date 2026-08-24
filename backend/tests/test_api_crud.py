import uuid

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, Schedule, ScheduleVersion


async def _exercise_crud(
    client: AsyncClient,
    tenant_id: str,
    resource: str,
    payload: dict[str, object],
) -> dict[str, object]:
    headers = {"X-Tenant-ID": tenant_id}
    created = await client.post(f"/api/v1/{resource}", headers=headers, json=payload)
    assert created.status_code == 201, created.text
    body = created.json()

    fetched = await client.get(f"/api/v1/{resource}/{body['id']}", headers=headers)
    assert fetched.status_code == 200

    updated = await client.patch(
        f"/api/v1/{resource}/{body['id']}",
        headers=headers,
        json={"status": "approved"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "approved"

    listed = await client.get(f"/api/v1/{resource}", headers=headers)
    assert listed.status_code == 200
    assert any(item["id"] == body["id"] for item in listed.json())
    return body


async def test_all_requested_crud_apis(client: AsyncClient, db_session: AsyncSession) -> None:
    tenant = Organization(name="API Tenant", code="API-TENANT")
    db_session.add(tenant)
    await db_session.flush()
    tenant_id = str(tenant.id)

    project = await _exercise_crud(
        client,
        tenant_id,
        "projects",
        {"name": "Project A", "code": "PROJECT-A"},
    )
    schedule = Schedule(
        tenant_id=tenant.id,
        project_id=uuid.UUID(str(project["id"])),
        name="API Schedule",
    )
    db_session.add(schedule)
    await db_session.flush()
    version = ScheduleVersion(
        tenant_id=tenant.id,
        schedule_id=schedule.id,
        version_number=1,
    )
    db_session.add(version)
    await db_session.flush()

    payloads: dict[str, dict[str, object]] = {
        "activities": {
            "schedule_version_id": str(version.id),
            "name": "Activity A45",
            "code": "A45",
        },
        "suppliers": {"name": "Supplier Z", "code": "SUPPLIER-Z"},
        "materials": {"name": "Material M42", "code": "M42", "unit": "tonne"},
        "contracts": {
            "project_id": project["id"],
            "number": "C234",
            "title": "Main Contract",
            "contract_type": "main",
        },
        "risks": {
            "project_id": project["id"],
            "code": "R17",
            "title": "Risk R17",
        },
        "delays": {
            "project_id": project["id"],
            "code": "D5",
            "title": "Delay D5",
        },
        "documents": {
            "project_id": project["id"],
            "number": "DOC-1",
            "title": "Project Document",
            "document_type": "report",
        },
    }
    records = {
        resource: await _exercise_crud(client, tenant_id, resource, payload)
        for resource, payload in payloads.items()
    }

    other_tenant = Organization(name="Other", code="OTHER-TENANT")
    db_session.add(other_tenant)
    await db_session.flush()
    hidden = await client.get(
        f"/api/v1/risks/{records['risks']['id']}",
        headers={"X-Tenant-ID": str(other_tenant.id)},
    )
    assert hidden.status_code == 404

    for resource, record in reversed(list(records.items())):
        deleted = await client.delete(
            f"/api/v1/{resource}/{record['id']}",
            headers={"X-Tenant-ID": tenant_id},
        )
        assert deleted.status_code == 204
