import uuid
from typing import Annotated

from fastapi import Depends, Header


async def get_tenant_id(
    x_tenant_id: Annotated[uuid.UUID, Header(alias="X-Tenant-ID")],
) -> uuid.UUID:
    return x_tenant_id


TenantId = Annotated[uuid.UUID, Depends(get_tenant_id)]
