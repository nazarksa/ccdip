Continue the existing project.

Implement a production-quality ingestion framework.

==================================================
SUPPORTED INPUTS
================

Initially support:

CSV
Excel
JSON
REST API

Design adapters for future:

Primavera P6/XER
ERP
BIM/IFC
document management systems

==================================================
PIPELINE
========

Every ingestion must follow:

SOURCE

↓

EXTRACT

↓

VALIDATE

↓

NORMALIZE

↓

MAP

↓

ENTITY RESOLUTION

↓

POSTGRESQL

↓

NEO4J

↓

PROVENANCE

↓

EVENT

==================================================
ENTITY RESOLUTION
=================

Implement canonical entity matching.

Handle examples such as:

ABC Construction
ABC Construction Co.
ABC Construction Company Ltd.

Support:

exact matching

normalized matching

fuzzy matching

identifier matching

semantic matching foundation

human review

==================================================
PROVENANCE
==========

Every imported record must track:

source_system

source_record_id

source_file

import_batch

imported_at

==================================================
DATA QUALITY
============

Detect:

duplicates

missing references

invalid dates

orphan records

invalid relationships

stale records

==================================================
BACKGROUND JOBS
===============

Use Redis-backed workers or equivalent.

Long-running imports must not block API requests.

==================================================
TESTING
=======

Create realistic test files.

Test the full ingestion lifecycle.

==================================================
ACCEPTANCE
==========

Importing a project dataset creates:

PostgreSQL records

Neo4j relationships

provenance

data-quality results

and is repeatable/idempotent.
