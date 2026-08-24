from sqlalchemy import Uuid, inspect

from app.db.base import Base
from app.models import Activity, Contract, Document, Project, Supplier


def test_all_transactional_entities_are_registered() -> None:
    expected_tables = {
        "organizations",
        "projects",
        "activities",
        "contracts",
        "suppliers",
        "materials",
        "risks",
        "delays",
        "documents",
        "payments",
        "evidence",
    }
    assert expected_tables <= set(Base.metadata.tables)
    assert len(Base.metadata.tables) == 62


def test_tenant_entities_have_common_transactional_columns() -> None:
    for model in (Project, Activity, Contract, Supplier, Document):
        columns = inspect(model).columns
        assert {
            "id",
            "tenant_id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "status",
        } <= {column.key for column in columns}
        assert isinstance(columns.id.type, Uuid)
        assert columns.tenant_id.index is True


def test_domain_uniqueness_is_scoped_correctly() -> None:
    project_constraints = {
        tuple(column.name for column in constraint.columns)
        for constraint in Project.__table__.constraints
        if hasattr(constraint, "columns")
    }
    assert ("tenant_id", "code") in project_constraints
