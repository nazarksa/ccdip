import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantEntity


class Contract(TenantEntity, Base):
    __tablename__ = "contracts"
    __table_args__ = (UniqueConstraint("tenant_id", "number"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    number: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    contract_type: Mapped[str] = mapped_column(String(50), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="SAR")
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)


class ContractParty(TenantEntity, Base):
    __tablename__ = "contract_parties"
    __table_args__ = (UniqueConstraint("contract_id", "party_type", "name"),)

    contract_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="RESTRICT"), index=True
    )
    supplier_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    party_type: Mapped[str] = mapped_column(String(50), nullable=False)


class Subcontract(TenantEntity, Base):
    __tablename__ = "subcontracts"
    __table_args__ = (UniqueConstraint("tenant_id", "number"),)

    contract_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subcontractor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    number: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)


class PurchaseOrder(TenantEntity, Base):
    __tablename__ = "purchase_orders"
    __table_args__ = (UniqueConstraint("tenant_id", "number"),)

    contract_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("contracts.id", ondelete="SET NULL"), index=True
    )
    supplier_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    number: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="SAR")
    order_date: Mapped[date | None] = mapped_column(Date)


class ChangeOrder(TenantEntity, Base):
    __tablename__ = "change_orders"
    __table_args__ = (UniqueConstraint("contract_id", "number"),)

    contract_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    number: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    reason: Mapped[str | None] = mapped_column(Text)


class Claim(TenantEntity, Base):
    __tablename__ = "claims"
    __table_args__ = (UniqueConstraint("contract_id", "number"),)

    contract_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    number: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    claimed_amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    description: Mapped[str | None] = mapped_column(Text)
