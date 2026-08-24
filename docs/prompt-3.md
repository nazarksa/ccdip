Continue the existing project.

Your task is to implement the first-class Construction Knowledge Graph in Neo4j.

==================================================

1. CORE PRINCIPLE
   ==================================================

PostgreSQL = transactional truth.

Neo4j = relationship intelligence.

Do not duplicate entire relational records inside Neo4j.

Use stable UUIDs to reference PostgreSQL entities.

==================================================
2. NODE TYPES
=============

Implement graph representations for:

Organization
Project
Program
Package
Site
Zone
Building
Activity
Milestone
Contract
Contractor
Subcontractor
Supplier
Factory
Material
Equipment
Asset
Risk
Delay
RFI
Submittal
Invoice
Payment
Document
Employee
Regulation

==================================================
3. RELATIONSHIPS
================

Implement relationships such as:

Project -> HAS_CONTRACT -> Contract

Contract -> AWARDED_TO -> Contractor

Contractor -> SUBCONTRACTS_TO -> Subcontractor

Subcontractor -> PROCURES_FROM -> Supplier

Supplier -> PRODUCES -> Material

Supplier -> DEPENDS_ON -> Factory

Project -> CONTAINS -> Building

Building -> REQUIRES -> Material

Activity -> USES -> Material

Activity -> DEPENDS_ON -> Activity

Activity -> BLOCKED_BY -> Delay

Delay -> CONTRIBUTED_TO_BY -> Risk

Risk -> AFFECTS -> Project

Project -> USES -> Equipment

Invoice -> FOR_CONTRACT -> Contract

Payment -> SETTLES -> Invoice

RFI -> BLOCKS -> Activity

Submittal -> REQUIRED_FOR -> Activity

==================================================
4. RELATIONSHIP METADATA
========================

Every graph relationship must support metadata where applicable:

relationship_id
confidence
source_system
source_record_id
source_document_id
evidence_id
created_at
valid_from
valid_to
extraction_method
human_verified

==================================================
5. TEMPORAL GRAPH
=================

The graph must support temporal validity.

A relationship may change over time.

Support:

valid_from
valid_to

and where necessary:

planned
forecast
actual
baseline

==================================================
6. CONSTRAINTS
==============

Create appropriate Neo4j constraints and indexes.

Use stable UUIDs.

==================================================
7. GRAPH SERVICE
================

Create a Python graph abstraction.

Do NOT scatter Cypher throughout the application.

Create a dedicated graph layer.

Examples:

GraphRepository

GraphService

ProjectGraphService

DependencyGraphService

==================================================
8. SAFE QUERIES
===============

Do not expose unrestricted Cypher execution to AI.

Create parameterized graph methods.

Examples:

get_project_neighbors()
get_upstream_dependencies()
get_downstream_dependencies()
get_supplier_projects()
get_activity_dependencies()
get_causal_candidates()

==================================================
9. SYNCHRONIZATION
==================

Create a service capable of synchronizing PostgreSQL entities into Neo4j.

The synchronization must be idempotent.

==================================================
10. TEST DATA
=============

Populate the following chain:

Project A
→ Contractor X
→ Supplier Z
→ Material M42
→ Activity A45
→ Building B
→ Milestone M17

Also:

Supplier Z
→ Project B

Supplier Z
→ Project C

Supplier Z
→ Factory F3

==================================================
11. TESTING
===========

Test:

node creation

relationship creation

relationship metadata

temporal properties

idempotent synchronization

graph traversal

tenant isolation

==================================================
12. ACCEPTANCE
==============

Given Project A, the graph can traverse:

Project A
→ Contractor X
→ Supplier Z
→ Material M42
→ Activity A45
→ Building B
→ Milestone M17

and Supplier Z can be identified as a dependency shared by multiple projects.

Do not implement the AI layer yet.
