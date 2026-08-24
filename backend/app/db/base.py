import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """Declarative base for PostgreSQL models."""


class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class TenantMixin:
    @declared_attr
    def tenant_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(
            Uuid, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
        )


class AuditMixin:
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active", index=True)

    @declared_attr
    def created_by(cls) -> Mapped[uuid.UUID | None]:
        return mapped_column(
            Uuid,
            ForeignKey(
                "users.id",
                ondelete="SET NULL",
                use_alter=True,
                name=f"fk_{getattr(cls, '__tablename__')}_created_by_users",  # noqa: B009
            ),
            nullable=True,
        )

    @declared_attr
    def updated_by(cls) -> Mapped[uuid.UUID | None]:
        return mapped_column(
            Uuid,
            ForeignKey(
                "users.id",
                ondelete="SET NULL",
                use_alter=True,
                name=f"fk_{getattr(cls, '__tablename__')}_updated_by_users",  # noqa: B009
            ),
            nullable=True,
        )


class TenantEntity(UUIDPrimaryKeyMixin, TenantMixin, TimestampMixin, AuditMixin):
    """Common columns for tenant-owned transactional records."""

    __abstract__ = True
