import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantEntity


class Program(TenantEntity, Base):
    __tablename__ = "programs"
    __table_args__ = (UniqueConstraint("tenant_id", "code"),)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class Project(TenantEntity, Base):
    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("tenant_id", "code"),)

    program_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("programs.id", ondelete="SET NULL"), index=True
    )
    business_unit_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("business_units.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)


class SubProject(TenantEntity, Base):
    __tablename__ = "subprojects"
    __table_args__ = (UniqueConstraint("project_id", "code"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)


class Package(TenantEntity, Base):
    __tablename__ = "packages"
    __table_args__ = (UniqueConstraint("project_id", "code"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subproject_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("subprojects.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)


class Phase(TenantEntity, Base):
    __tablename__ = "phases"
    __table_args__ = (UniqueConstraint("project_id", "code"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    sequence: Mapped[int] = mapped_column(nullable=False, default=0)


class Site(TenantEntity, Base):
    __tablename__ = "sites"
    __table_args__ = (UniqueConstraint("project_id", "code"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str | None] = mapped_column(String(500))


class Zone(TenantEntity, Base):
    __tablename__ = "zones"
    __table_args__ = (UniqueConstraint("site_id", "code"),)

    site_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)


class Building(TenantEntity, Base):
    __tablename__ = "buildings"
    __table_args__ = (UniqueConstraint("site_id", "code"),)

    site_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True
    )
    zone_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("zones.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
