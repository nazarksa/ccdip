import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantEntity


class Schedule(TenantEntity, Base):
    __tablename__ = "schedules"
    __table_args__ = (UniqueConstraint("project_id", "name"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class ScheduleVersion(TenantEntity, Base):
    __tablename__ = "schedule_versions"
    __table_args__ = (UniqueConstraint("schedule_id", "version_number"),)

    schedule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(nullable=False)
    data_date: Mapped[date | None] = mapped_column(Date)


class Baseline(TenantEntity, Base):
    __tablename__ = "baselines"
    __table_args__ = (UniqueConstraint("schedule_id", "name"),)

    schedule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False, index=True
    )
    schedule_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("schedule_versions.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class WBS(TenantEntity, Base):
    __tablename__ = "wbs"
    __table_args__ = (UniqueConstraint("schedule_version_id", "code"),)

    schedule_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("schedule_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("wbs.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)


class Calendar(TenantEntity, Base):
    __tablename__ = "calendars"
    __table_args__ = (UniqueConstraint("project_id", "name"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="UTC")
    working_pattern: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)


class Activity(TenantEntity, Base):
    __tablename__ = "activities"
    __table_args__ = (UniqueConstraint("schedule_version_id", "code"),)

    schedule_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("schedule_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    wbs_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("wbs.id", ondelete="SET NULL"), index=True
    )
    calendar_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("calendars.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    planned_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    planned_finish: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_finish: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    percent_complete: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)


class Milestone(TenantEntity, Base):
    __tablename__ = "milestones"
    __table_args__ = (UniqueConstraint("schedule_version_id", "code"),)

    schedule_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("schedule_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    activity_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("activities.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Resource(TenantEntity, Base):
    __tablename__ = "resources"
    __table_args__ = (UniqueConstraint("project_id", "code"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)


class ActivityDependency(TenantEntity, Base):
    __tablename__ = "activity_dependencies"
    __table_args__ = (UniqueConstraint("predecessor_id", "successor_id", "dependency_type"),)

    predecessor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    successor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    dependency_type: Mapped[str] = mapped_column(String(2), nullable=False, default="FS")
    lag_days: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
