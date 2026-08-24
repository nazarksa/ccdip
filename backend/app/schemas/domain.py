import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, create_model


class EntityCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: str = Field(default="active", max_length=32)


class EntityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    created_by: uuid.UUID | None
    updated_by: uuid.UUID | None
    status: str


class OrganizationCreate(BaseModel):
    name: str
    code: str
    status: str = "active"


class OrganizationUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    status: str | None = None


class OrganizationRead(OrganizationCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PermissionCreate(BaseModel):
    code: str
    description: str | None = None


class PermissionUpdate(BaseModel):
    code: str | None = None
    description: str | None = None


class PermissionRead(PermissionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


FieldSpec = dict[str, tuple[Any, Any]]


def _schemas(
    name: str, fields: FieldSpec
) -> tuple[type[BaseModel], type[BaseModel], type[BaseModel]]:
    create = create_model(  # type: ignore[call-overload]
        f"{name}Create", __base__=EntityCreate, **fields
    )
    update_fields = {
        field_name: (field_type | None, None)
        for field_name, (field_type, _default) in fields.items()
    }
    update = create_model(  # type: ignore[call-overload]
        f"{name}Update",
        __base__=BaseModel,
        status=(str | None, None),
        **update_fields,
    )
    read = create_model(  # type: ignore[call-overload]
        f"{name}Read", __base__=EntityRead, **fields
    )
    return create, update, read


SCHEMAS: dict[str, tuple[type[BaseModel], type[BaseModel], type[BaseModel]]] = {}


def _register(name: str, fields: FieldSpec) -> None:
    schemas = _schemas(name, fields)
    SCHEMAS[name] = schemas
    globals()[f"{name}Create"], globals()[f"{name}Update"], globals()[f"{name}Read"] = schemas


optional_uuid = (uuid.UUID | None, None)
optional_str = (str | None, None)
optional_date = (date | None, None)
optional_datetime = (datetime | None, None)

_register("BusinessUnit", {"name": (str, ...), "code": (str, ...)})
_register(
    "Department",
    {"business_unit_id": (uuid.UUID, ...), "name": (str, ...), "code": (str, ...)},
)
_register(
    "User",
    {"department_id": optional_uuid, "email": (str, ...), "full_name": (str, ...)},
)
_register("Role", {"name": (str, ...), "description": optional_str})
_register("Program", {"name": (str, ...), "code": (str, ...), "description": optional_str})
_register(
    "Project",
    {
        "program_id": optional_uuid,
        "business_unit_id": optional_uuid,
        "name": (str, ...),
        "code": (str, ...),
        "description": optional_str,
        "start_date": optional_date,
        "end_date": optional_date,
    },
)
_register("SubProject", {"project_id": (uuid.UUID, ...), "name": (str, ...), "code": (str, ...)})
_register(
    "Package",
    {
        "project_id": (uuid.UUID, ...),
        "subproject_id": optional_uuid,
        "name": (str, ...),
        "code": (str, ...),
    },
)
_register(
    "Phase",
    {
        "project_id": (uuid.UUID, ...),
        "name": (str, ...),
        "code": (str, ...),
        "sequence": (int, 0),
    },
)
_register(
    "Site",
    {
        "project_id": (uuid.UUID, ...),
        "name": (str, ...),
        "code": (str, ...),
        "address": optional_str,
    },
)
_register("Zone", {"site_id": (uuid.UUID, ...), "name": (str, ...), "code": (str, ...)})
_register(
    "Building",
    {"site_id": (uuid.UUID, ...), "zone_id": optional_uuid, "name": (str, ...), "code": (str, ...)},
)
_register(
    "Schedule", {"project_id": (uuid.UUID, ...), "name": (str, ...), "description": optional_str}
)
_register(
    "ScheduleVersion",
    {"schedule_id": (uuid.UUID, ...), "version_number": (int, ...), "data_date": optional_date},
)
_register(
    "Baseline",
    {
        "schedule_id": (uuid.UUID, ...),
        "schedule_version_id": (uuid.UUID, ...),
        "name": (str, ...),
        "approved_at": optional_datetime,
    },
)
_register(
    "WBS",
    {
        "schedule_version_id": (uuid.UUID, ...),
        "parent_id": optional_uuid,
        "name": (str, ...),
        "code": (str, ...),
    },
)
_register(
    "Calendar",
    {
        "project_id": (uuid.UUID, ...),
        "name": (str, ...),
        "timezone": (str, "UTC"),
        "working_pattern": (dict[str, object], {}),
    },
)
_register(
    "Activity",
    {
        "schedule_version_id": (uuid.UUID, ...),
        "wbs_id": optional_uuid,
        "calendar_id": optional_uuid,
        "name": (str, ...),
        "code": (str, ...),
        "planned_start": optional_datetime,
        "planned_finish": optional_datetime,
        "actual_start": optional_datetime,
        "actual_finish": optional_datetime,
        "percent_complete": (Decimal, Decimal("0")),
    },
)
_register(
    "Milestone",
    {
        "schedule_version_id": (uuid.UUID, ...),
        "activity_id": optional_uuid,
        "name": (str, ...),
        "code": (str, ...),
        "due_at": optional_datetime,
    },
)
_register(
    "Resource",
    {
        "project_id": (uuid.UUID, ...),
        "name": (str, ...),
        "code": (str, ...),
        "resource_type": (str, ...),
    },
)
_register(
    "ActivityDependency",
    {
        "predecessor_id": (uuid.UUID, ...),
        "successor_id": (uuid.UUID, ...),
        "dependency_type": (str, "FS"),
        "lag_days": (Decimal, Decimal("0")),
    },
)
_register(
    "Contract",
    {
        "project_id": (uuid.UUID, ...),
        "number": (str, ...),
        "title": (str, ...),
        "contract_type": (str, ...),
        "value": (Decimal, Decimal("0")),
        "currency": (str, "SAR"),
        "start_date": optional_date,
        "end_date": optional_date,
    },
)
_register(
    "ContractParty",
    {
        "contract_id": (uuid.UUID, ...),
        "organization_id": optional_uuid,
        "supplier_id": optional_uuid,
        "name": (str, ...),
        "party_type": (str, ...),
    },
)
_register(
    "Subcontract",
    {
        "contract_id": (uuid.UUID, ...),
        "subcontractor_id": (uuid.UUID, ...),
        "number": (str, ...),
        "title": (str, ...),
        "value": (Decimal, Decimal("0")),
    },
)
_register(
    "PurchaseOrder",
    {
        "contract_id": optional_uuid,
        "supplier_id": (uuid.UUID, ...),
        "number": (str, ...),
        "value": (Decimal, Decimal("0")),
        "currency": (str, "SAR"),
        "order_date": optional_date,
    },
)
_register(
    "ChangeOrder",
    {
        "contract_id": (uuid.UUID, ...),
        "number": (str, ...),
        "title": (str, ...),
        "value": (Decimal, Decimal("0")),
        "reason": optional_str,
    },
)
_register(
    "Claim",
    {
        "contract_id": (uuid.UUID, ...),
        "number": (str, ...),
        "title": (str, ...),
        "claimed_amount": (Decimal, Decimal("0")),
        "description": optional_str,
    },
)
_register(
    "Supplier",
    {
        "name": (str, ...),
        "code": (str, ...),
        "tax_id": optional_str,
        "contact_email": optional_str,
    },
)
_register(
    "Manufacturer",
    {"supplier_id": optional_uuid, "name": (str, ...), "code": (str, ...)},
)
_register(
    "Factory",
    {
        "manufacturer_id": (uuid.UUID, ...),
        "name": (str, ...),
        "code": (str, ...),
        "location": optional_str,
    },
)
_register(
    "Material",
    {
        "manufacturer_id": optional_uuid,
        "name": (str, ...),
        "code": (str, ...),
        "unit": (str, ...),
        "description": optional_str,
    },
)
_register(
    "Product",
    {
        "material_id": (uuid.UUID, ...),
        "manufacturer_id": optional_uuid,
        "name": (str, ...),
        "sku": (str, ...),
    },
)
_register(
    "Shipment",
    {
        "supplier_id": (uuid.UUID, ...),
        "factory_id": optional_uuid,
        "project_id": (uuid.UUID, ...),
        "tracking_number": (str, ...),
        "shipped_at": optional_datetime,
        "expected_at": optional_date,
    },
)
_register(
    "Delivery",
    {
        "shipment_id": (uuid.UUID, ...),
        "warehouse_id": optional_uuid,
        "material_id": (uuid.UUID, ...),
        "delivery_number": (str, ...),
        "quantity": (Decimal, ...),
        "delivered_at": optional_datetime,
    },
)
_register(
    "Warehouse",
    {
        "project_id": optional_uuid,
        "name": (str, ...),
        "code": (str, ...),
        "location": optional_str,
    },
)
_register(
    "Equipment",
    {
        "project_id": (uuid.UUID, ...),
        "name": (str, ...),
        "code": (str, ...),
        "equipment_type": (str, ...),
    },
)
_register(
    "Asset",
    {
        "project_id": (uuid.UUID, ...),
        "equipment_id": optional_uuid,
        "building_id": optional_uuid,
        "name": (str, ...),
        "asset_tag": (str, ...),
    },
)
_register(
    "RFI",
    {
        "project_id": (uuid.UUID, ...),
        "number": (str, ...),
        "subject": (str, ...),
        "question": (str, ...),
        "response": optional_str,
        "due_at": optional_datetime,
    },
)
_register(
    "Submittal",
    {
        "project_id": (uuid.UUID, ...),
        "number": (str, ...),
        "title": (str, ...),
        "due_at": optional_datetime,
    },
)
for _name in ("Drawing", "Specification"):
    _register(
        _name,
        {
            "project_id": (uuid.UUID, ...),
            "number": (str, ...),
            "title": (str, ...),
            "revision": (str, ...),
            "file_uri": optional_str,
        },
    )
_register(
    "BIMModel",
    {
        "project_id": (uuid.UUID, ...),
        "name": (str, ...),
        "revision": (str, ...),
        "file_uri": (str, ...),
    },
)
_register(
    "BIMElement",
    {
        "bim_model_id": (uuid.UUID, ...),
        "building_id": optional_uuid,
        "external_id": (str, ...),
        "name": optional_str,
        "element_type": optional_str,
    },
)
_register("RiskCategory", {"name": (str, ...), "description": optional_str})
_register(
    "Risk",
    {
        "project_id": (uuid.UUID, ...),
        "category_id": optional_uuid,
        "code": (str, ...),
        "title": (str, ...),
        "description": optional_str,
        "probability": (Decimal, Decimal("0")),
        "impact": (Decimal, Decimal("0")),
    },
)
_register(
    "RiskMitigation",
    {
        "risk_id": (uuid.UUID, ...),
        "action": (str, ...),
        "owner_id": optional_uuid,
        "due_date": optional_date,
    },
)
_register(
    "Issue",
    {
        "project_id": (uuid.UUID, ...),
        "code": (str, ...),
        "title": (str, ...),
        "description": optional_str,
        "due_date": optional_date,
    },
)
_register(
    "Delay",
    {
        "project_id": (uuid.UUID, ...),
        "activity_id": optional_uuid,
        "code": (str, ...),
        "title": (str, ...),
        "description": optional_str,
        "start_date": optional_date,
        "end_date": optional_date,
        "delay_days": (Decimal, Decimal("0")),
    },
)
_register(
    "Inspection",
    {
        "project_id": (uuid.UUID, ...),
        "activity_id": optional_uuid,
        "number": (str, ...),
        "inspection_type": (str, ...),
        "inspected_at": optional_datetime,
        "result": optional_str,
    },
)
_register(
    "NCR",
    {
        "project_id": (uuid.UUID, ...),
        "inspection_id": optional_uuid,
        "number": (str, ...),
        "title": (str, ...),
        "description": optional_str,
    },
)
_register(
    "QualityEvent",
    {
        "project_id": (uuid.UUID, ...),
        "ncr_id": optional_uuid,
        "event_type": (str, ...),
        "description": (str, ...),
        "occurred_at": optional_datetime,
    },
)
_register(
    "Invoice",
    {
        "contract_id": (uuid.UUID, ...),
        "supplier_id": optional_uuid,
        "number": (str, ...),
        "amount": (Decimal, ...),
        "currency": (str, "SAR"),
        "invoice_date": optional_date,
        "due_date": optional_date,
    },
)
_register(
    "Payment",
    {
        "invoice_id": (uuid.UUID, ...),
        "reference": (str, ...),
        "amount": (Decimal, ...),
        "currency": (str, "SAR"),
        "payment_date": optional_date,
    },
)
_register(
    "Commitment",
    {
        "project_id": (uuid.UUID, ...),
        "contract_id": optional_uuid,
        "code": (str, ...),
        "description": optional_str,
        "amount": (Decimal, ...),
        "currency": (str, "SAR"),
    },
)
_register(
    "Document",
    {
        "project_id": (uuid.UUID, ...),
        "contract_id": optional_uuid,
        "number": (str, ...),
        "title": (str, ...),
        "document_type": (str, ...),
    },
)
_register(
    "DocumentVersion",
    {
        "document_id": (uuid.UUID, ...),
        "version_number": (int, ...),
        "file_uri": (str, ...),
        "checksum": optional_str,
        "mime_type": optional_str,
    },
)
_register(
    "DocumentChunk",
    {"document_version_id": (uuid.UUID, ...), "chunk_index": (int, ...), "content": (str, ...)},
)
_register(
    "Evidence",
    {
        "document_version_id": (uuid.UUID, ...),
        "title": (str, ...),
        "description": optional_str,
        "source_page": (int | None, None),
    },
)
