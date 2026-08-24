from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, Project
from app.repositories.tenant import TenantRepository


async def test_repository_enforces_tenant_scope(db_session: AsyncSession) -> None:
    first_tenant = Organization(name="First", code="FIRST")
    second_tenant = Organization(name="Second", code="SECOND")
    db_session.add_all([first_tenant, second_tenant])
    await db_session.flush()

    repository = TenantRepository(Project, db_session)
    project = await repository.create(first_tenant.id, {"name": "Project A", "code": "A"})

    assert await repository.get(first_tenant.id, project.id) is project
    assert await repository.get(second_tenant.id, project.id) is None
    assert await repository.list(second_tenant.id) == []


async def test_repository_soft_delete_hides_record(db_session: AsyncSession) -> None:
    tenant = Organization(name="Tenant", code="TENANT")
    db_session.add(tenant)
    await db_session.flush()
    repository = TenantRepository(Project, db_session)
    project = await repository.create(tenant.id, {"name": "Delete Me", "code": "DELETE"})

    await repository.soft_delete(project)

    assert project.status == "deleted"
    assert await repository.get(tenant.id, project.id) is None
