import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantEntity


class Equipment(TenantEntity, Base):
    __tablename__ = "equipment"
    __table_args__ = (UniqueConstraint("tenant_id", "code"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    equipment_type: Mapped[str] = mapped_column(String(100), nullable=False)


class Asset(TenantEntity, Base):
    __tablename__ = "assets"
    __table_args__ = (UniqueConstraint("tenant_id", "asset_tag"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    equipment_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("equipment.id", ondelete="SET NULL"), index=True
    )
    building_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("buildings.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    asset_tag: Mapped[str] = mapped_column(String(100), nullable=False)


class RFI(TenantEntity, Base):
    __tablename__ = "rfis"
    __table_args__ = (UniqueConstraint("project_id", "number"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    number: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[str] = mapped_column(String(250), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str | None] = mapped_column(Text)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Submittal(TenantEntity, Base):
    __tablename__ = "submittals"
    __table_args__ = (UniqueConstraint("project_id", "number"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    number: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Drawing(TenantEntity, Base):
    __tablename__ = "drawings"
    __table_args__ = (UniqueConstraint("project_id", "number", "revision"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    number: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    revision: Mapped[str] = mapped_column(String(30), nullable=False)
    file_uri: Mapped[str | None] = mapped_column(String(1000))


class Specification(TenantEntity, Base):
    __tablename__ = "specifications"
    __table_args__ = (UniqueConstraint("project_id", "number", "revision"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    number: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    revision: Mapped[str] = mapped_column(String(30), nullable=False)
    file_uri: Mapped[str | None] = mapped_column(String(1000))


class BIMModel(TenantEntity, Base):
    __tablename__ = "bim_models"
    __table_args__ = (UniqueConstraint("project_id", "name", "revision"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    revision: Mapped[str] = mapped_column(String(30), nullable=False)
    file_uri: Mapped[str] = mapped_column(String(1000), nullable=False)


class BIMElement(TenantEntity, Base):
    __tablename__ = "bim_elements"
    __table_args__ = (UniqueConstraint("bim_model_id", "external_id"),)

    bim_model_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("bim_models.id", ondelete="CASCADE"), nullable=False, index=True
    )
    building_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("buildings.id", ondelete="SET NULL"), index=True
    )
    external_id: Mapped[str] = mapped_column(String(200), nullable=False)
    name: Mapped[str | None] = mapped_column(String(250))
    element_type: Mapped[str | None] = mapped_column(String(100))
