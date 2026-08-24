import uuid
from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.identity import Organization

FALLBACK_TENANT_ID = uuid.UUID("2039fb7b-898e-4ac7-a0d7-36a7622a9e54")


async def get_tenant_id(
    x_tenant_id: Annotated[uuid.UUID | None, Header(alias="X-Tenant-ID")] = None,
    session: AsyncSession = Depends(get_session),
) -> uuid.UUID:
    if x_tenant_id is not None:
        return x_tenant_id
    result = await session.scalar(select(Organization.id))
    return result if result is not None else FALLBACK_TENANT_ID


TenantId = Annotated[uuid.UUID, Depends(get_tenant_id)]
