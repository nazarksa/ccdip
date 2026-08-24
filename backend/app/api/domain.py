from fastapi import APIRouter

from app.api.crud import create_crud_router
from app.models import Activity, Contract, Delay, Document, Material, Project, Risk, Supplier
from app.schemas.domain import SCHEMAS

router = APIRouter()

for path, tag, model in (
    ("projects", "Projects", Project),
    ("activities", "Activities", Activity),
    ("suppliers", "Suppliers", Supplier),
    ("materials", "Materials", Material),
    ("contracts", "Contracts", Contract),
    ("risks", "Risks", Risk),
    ("delays", "Delays", Delay),
    ("documents", "Documents", Document),
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
