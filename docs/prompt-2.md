Continue the existing project.

Do NOT redesign the architecture unless absolutely necessary.

Your task is to implement the transactional construction domain model in PostgreSQL.

==================================================

1. PRINCIPLE
   ==================================================

PostgreSQL is the source of transactional truth.

Neo4j will later handle relationship intelligence.

Do NOT put the graph model into PostgreSQL unnecessarily.

==================================================
2. CORE ENTITIES
================

Implement proper SQLAlchemy models and Pydantic schemas for:

Organization
BusinessUnit
Department
User
Role
Permission

Program
Project
SubProject
Package
Phase
Site
Zone
Building

Schedule
ScheduleVersion
Baseline
WBS
Activity
Milestone
Calendar
Resource
ActivityDependency

Contract
ContractParty
Subcontract
PurchaseOrder
ChangeOrder
Claim

Supplier
Manufacturer
Factory
Material
Product
Shipment
Delivery
Warehouse

Equipment
Asset

RFI
Submittal
Drawing
Specification
BIMModel
BIMElement

Risk
RiskCategory
RiskMitigation
Issue
Delay

Inspection
NCR
QualityEvent

Invoice
Payment
Commitment

Document
DocumentVersion
DocumentChunk
Evidence

==================================================
3. COMMON FIELDS
================

Use UUID identifiers.

Where appropriate include:

id
tenant_id
created_at
updated_at
created_by
updated_by
status

Use proper foreign keys.

Use indexes.

Use unique constraints.

Use soft deletion only where appropriate.

==================================================
4. TENANCY
==========

All tenant-owned records must contain tenant_id.

Design the model so tenant isolation can be enforced at the service/repository layer.

==================================================
5. MIGRATIONS
=============

Create Alembic migrations.

Database must be reproducible from an empty database.

==================================================
6. SEED DATA
============

Create a small development dataset.

Include:

Project A
Contractor X
Subcontractor Y
Supplier Z
Factory F3
Material M42
Building B
Activity A45
Milestone M17
Risk R17
Delay D5
Contract C234
Invoice I993
Payment P883

Do NOT implement the causal engine yet.

The seed data should simply establish legitimate transactional records.

==================================================
7. API
======

Create basic CRUD APIs for:

projects
activities
suppliers
materials
contracts
risks
delays
documents

Keep API structure clean.

==================================================
8. TESTING
==========

Create:

model tests
migration tests
repository tests
API tests

==================================================
9. ACCEPTANCE
=============

A clean database can be created from scratch.

Migrations run.

Seed data loads.

CRUD APIs work.

Tests pass.

Do not implement AI or graph intelligence yet.
