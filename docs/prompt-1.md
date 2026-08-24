You are the Principal Software Architect for this project.

We are building a production-grade Saudi Construction / Giga-Project Causality & Dependency Intelligence Platform.

This is NOT a toy project, tutorial, university assignment, or prototype.

The system will eventually combine:

* Python
* FastAPI
* PostgreSQL
* Neo4j
* Redis
* pgvector
* LangChain
* LangGraph
* Azure OpenAI
* React
* TypeScript
* Vite
* TanStack Query
* Zustand where appropriate
* Tailwind
* enterprise authentication/RBAC
* graph analytics
* schedule intelligence
* causal analysis
* risk propagation
* scenario simulation
* document intelligence
* GraphRAG

Your task in this phase is ONLY to establish the architecture and repository foundation.

DO NOT implement the complete application yet.

==================================================

1. ARCHITECTURE
   ==================================================

Design a modular enterprise architecture.

Prefer a modular monolith initially rather than premature microservices.

Backend responsibilities:

* API
* authentication
* authorization
* domain logic
* PostgreSQL persistence
* Neo4j graph
* background jobs
* document ingestion
* AI orchestration
* graph analytics
* schedule analytics
* causality
* risk
* scenarios
* audit
* observability

Frontend responsibilities:

* enterprise dashboard
* project 360
* graph visualization
* schedule visualization
* AI copilot
* risk
* supply chain
* contracts
* documents
* scenarios
* administration

==================================================
2. CREATE REPOSITORY STRUCTURE
==============================

Create a clean monorepo:

/backend
/frontend
/infra
/docs
/scripts
/tests

Backend should be organized approximately as:

backend/app/

api/
core/
config/
security/
db/
models/
schemas/
repositories/
services/
domain/
graph/
schedule/
causality/
risk/
supply_chain/
contracts/
documents/
ai/
agents/
workflows/
tools/
events/
analytics/
ingestion/
notifications/
audit/
workers/

Frontend:

frontend/src/

app/
components/
features/
pages/
layouts/
routes/
api/
hooks/
stores/
types/
lib/
graph/
charts/
gantt/
ai/
auth/
i18n/

Do not create unnecessary abstractions.

==================================================
3. DEVELOPMENT INFRASTRUCTURE
=============================

Create:

docker-compose.yml

.env.example

Dockerfiles

Makefile or equivalent task runner

README.md

backend README

frontend README

local development instructions

basic CI configuration

==================================================
4. LOCAL SERVICES
=================

Prepare Docker services for:

* PostgreSQL
* pgvector
* Neo4j
* Redis

Object storage can initially use an S3-compatible local service if useful.

==================================================
5. PYTHON
=========

Use Python 3.12+.

Use:

FastAPI
Pydantic v2
SQLAlchemy 2
Alembic
pytest
ruff
mypy where practical

Use async architecture where beneficial.

==================================================
6. FRONTEND
===========

Use:

Vite
React
TypeScript
React Router
TanStack Query
Tailwind
shadcn/ui or equivalent enterprise component system

==================================================
7. CONFIGURATION
================

Create typed configuration.

Environment variables must include placeholders for:

DATABASE_URL
NEO4J_URI
NEO4J_USERNAME
NEO4J_PASSWORD
REDIS_URL

AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_API_VERSION
AZURE_OPENAI_CHAT_DEPLOYMENT
AZURE_OPENAI_EMBEDDING_DEPLOYMENT

STORAGE_ENDPOINT
STORAGE_BUCKET

Do not hardcode secrets.

==================================================
8. HEALTH CHECK
===============

Implement:

GET /health

GET /ready

Readiness should eventually verify dependencies.

For now create the architecture cleanly.

==================================================
9. DOCUMENTATION
================

Create:

/docs/ARCHITECTURE.md
/docs/DECISIONS.md
/docs/DEVELOPMENT.md

Document:

* architecture
* technology decisions
* repository structure
* local development
* future modules

==================================================
10. IMPORTANT
=============

Do NOT implement:

* AI agents
* graph algorithms
* schedule engine
* causality
* risk engine
* complex UI

Those come later.

==================================================
11. ACCEPTANCE CRITERIA
=======================

At the end:

1. Backend starts.
2. Frontend starts.
3. Docker infrastructure starts.
4. /health works.
5. /ready exists.
6. Environment configuration works.
7. Repository structure is clean.
8. README explains how to start everything.
9. Tests run successfully.
10. No fake business functionality has been created.

Before finishing, inspect the entire repository for structural problems.

Do not claim completion without running the application and tests.
