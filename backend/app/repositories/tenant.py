import uuid
from typing import Any, cast

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import TenantEntity


class TenantRepository[ModelT: TenantEntity]:
    """Tenant-scoped persistence operations; no query can cross tenant boundaries."""

    def __init__(self, model: type[ModelT], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    def _scope(self, tenant_id: uuid.UUID) -> Select[tuple[ModelT]]:
        return select(self.model).where(
            self.model.tenant_id == tenant_id,
            self.model.status != "deleted",
        )

    async def list(
        self, tenant_id: uuid.UUID, *, offset: int = 0, limit: int = 100
    ) -> list[ModelT]:
        result = await self.session.scalars(
            self._scope(tenant_id).order_by(self.model.created_at).offset(offset).limit(limit)
        )
        return list(result)

    async def get(self, tenant_id: uuid.UUID, entity_id: uuid.UUID) -> ModelT | None:
        return cast(
            ModelT | None,
            await self.session.scalar(self._scope(tenant_id).where(self.model.id == entity_id)),
        )

    async def create(self, tenant_id: uuid.UUID, values: dict[str, Any]) -> ModelT:
        entity = self.model()
        entity.tenant_id = tenant_id
        for key, value in values.items():
            setattr(entity, key, value)
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity: ModelT, values: dict[str, Any]) -> ModelT:
        for key, value in values.items():
            setattr(entity, key, value)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def soft_delete(self, entity: ModelT) -> None:
        entity.status = "deleted"
        await self.session.flush()
