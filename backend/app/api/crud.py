import uuid
from typing import Annotated, Any, cast

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import TenantId
from app.db.session import get_session
from app.repositories.tenant import TenantRepository

Session = Annotated[AsyncSession, Depends(get_session)]


def create_crud_router(
    *,
    path: str,
    tag: str,
    model: type[Any],
    create_schema: type[BaseModel],
    update_schema: type[BaseModel],
    read_schema: type[BaseModel],
) -> APIRouter:
    router = APIRouter(prefix=f"/{path}", tags=[tag])

    async def list_entities(
        tenant_id: TenantId,
        session: Session,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=200)] = 100,
    ) -> list[Any]:
        return await TenantRepository(model, session).list(tenant_id, offset=offset, limit=limit)

    async def get_entity(entity_id: uuid.UUID, tenant_id: TenantId, session: Session) -> Any:
        entity = await TenantRepository(model, session).get(tenant_id, entity_id)
        if entity is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        return entity

    async def create_entity(
        payload: create_schema,  # type: ignore[valid-type]
        tenant_id: TenantId,
        session: Session,
    ) -> Any:
        try:
            validated = cast(BaseModel, payload)
            return await TenantRepository(model, session).create(tenant_id, validated.model_dump())
        except IntegrityError as exc:
            raise HTTPException(
                status_code=409, detail="Record conflicts with existing data"
            ) from exc

    async def update_entity(
        entity_id: uuid.UUID,
        payload: update_schema,  # type: ignore[valid-type]
        tenant_id: TenantId,
        session: Session,
    ) -> Any:
        repository = TenantRepository(model, session)
        entity = await repository.get(tenant_id, entity_id)
        if entity is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        try:
            validated = cast(BaseModel, payload)
            return await repository.update(entity, validated.model_dump(exclude_unset=True))
        except IntegrityError as exc:
            raise HTTPException(
                status_code=409, detail="Record conflicts with existing data"
            ) from exc

    async def delete_entity(
        entity_id: uuid.UUID, tenant_id: TenantId, session: Session
    ) -> Response:
        repository = TenantRepository(model, session)
        entity = await repository.get(tenant_id, entity_id)
        if entity is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        await repository.soft_delete(entity)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    router.add_api_route(
        "",
        list_entities,
        methods=["GET"],
        response_model=list[read_schema],  # type: ignore[valid-type]
    )
    router.add_api_route("/{entity_id}", get_entity, methods=["GET"], response_model=read_schema)
    router.add_api_route(
        "", create_entity, methods=["POST"], response_model=read_schema, status_code=201
    )
    router.add_api_route(
        "/{entity_id}", update_entity, methods=["PATCH"], response_model=read_schema
    )
    router.add_api_route("/{entity_id}", delete_entity, methods=["DELETE"], status_code=204)
    return router
