import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantEntity


class Supplier(TenantEntity, Base):
    __tablename__ = "suppliers"
    __table_args__ = (UniqueConstraint("tenant_id", "code"),)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    tax_id: Mapped[str | None] = mapped_column(String(100))
    contact_email: Mapped[str | None] = mapped_column(String(320))


class Manufacturer(TenantEntity, Base):
    __tablename__ = "manufacturers"
    __table_args__ = (UniqueConstraint("tenant_id", "code"),)

    supplier_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("suppliers.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)


class Factory(TenantEntity, Base):
    __tablename__ = "factories"
    __table_args__ = (UniqueConstraint("manufacturer_id", "code"),)

    manufacturer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("manufacturers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str | None] = mapped_column(String(500))


class Material(TenantEntity, Base):
    __tablename__ = "materials"
    __table_args__ = (UniqueConstraint("tenant_id", "code"),)

    manufacturer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("manufacturers.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class Product(TenantEntity, Base):
    __tablename__ = "products"
    __table_args__ = (UniqueConstraint("tenant_id", "sku"),)

    material_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("materials.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    manufacturer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("manufacturers.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), nullable=False)


class Warehouse(TenantEntity, Base):
    __tablename__ = "warehouses"
    __table_args__ = (UniqueConstraint("tenant_id", "code"),)

    project_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str | None] = mapped_column(String(500))


class Shipment(TenantEntity, Base):
    __tablename__ = "shipments"
    __table_args__ = (UniqueConstraint("tenant_id", "tracking_number"),)

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    factory_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("factories.id", ondelete="SET NULL"), index=True
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tracking_number: Mapped[str] = mapped_column(String(100), nullable=False)
    shipped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expected_at: Mapped[date | None] = mapped_column(Date)


class Delivery(TenantEntity, Base):
    __tablename__ = "deliveries"
    __table_args__ = (UniqueConstraint("tenant_id", "delivery_number"),)

    shipment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    warehouse_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("warehouses.id", ondelete="SET NULL"), index=True
    )
    material_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("materials.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    delivery_number: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
