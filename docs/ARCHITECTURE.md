# Architecture

## System shape

CCDI begins as a modular monolith. One deployable API owns transactional business behavior while
capability boundaries remain explicit in code and data access. This minimizes distributed-system
cost while preserving an extraction path for workloads that later demonstrate independent scaling,
availability, security, or release requirements.

The runtime consists of:

- React single-page application
- FastAPI API and application layer
- PostgreSQL with pgvector for transactional, relational, geospatial-ready, and vector data
- Neo4j for dependency and causal graph projections
- Redis for ephemeral coordination, caching, and job infrastructure
- S3-compatible object storage for source documents and generated artifacts
- background workers using the same application packages

PostgreSQL is the system of record unless a capability decision explicitly states otherwise. Neo4j
holds graph-native projections and analysis structures; graph writes must be traceable to source
records and safely replayable. Redis is never authoritative.

## Backend layering

Requests flow inward:

1. `api` validates transport concerns and invokes a use case.
2. `services` coordinates permissions, transactions, domain policies, and adapters.
3. Capability packages (`schedule`, `causality`, `risk`, and others) own business rules.
4. `repositories`, `db`, `graph`, `documents`, and provider integrations implement ports.
5. `events` captures meaningful state transitions for asynchronous consumers and audit.

Authentication identifies a principal. Authorization is enforced at use-case and data-access
boundaries, not only in routes. Future enterprise identity integration should use OIDC, map external
groups to platform roles, and support project-scoped permissions.

Long-running ingestion, analytics, document processing, and AI operations run outside request
handlers. API operations submit durable work and return an operation identifier. Workers must be
idempotent and observable.

## Frontend architecture

Routes compose pages from capability-oriented features. TanStack Query owns remote server state.
Local component state remains local; Zustand is reserved for genuinely shared client workflows.
API contracts should eventually be generated from OpenAPI. Graph and Gantt rendering are isolated
behind specialized boundaries because their performance and interaction models differ from forms
and dashboards.

The UI must support Arabic and English, right-to-left layout, Saudi locale/time-zone requirements,
accessible keyboard navigation, project-scoped authorization, and auditable administrative actions.

## Data and consistency

- PostgreSQL transactions protect authoritative state.
- An outbox pattern will publish reliable domain events when event consumers are introduced.
- Neo4j and search/vector indexes are eventually consistent projections.
- Object metadata and access policy live in PostgreSQL; binary content lives in object storage.
- Every derived insight must preserve provenance, model/version context, and source references.
- Tenant/project isolation must be part of schema and authorization design before business tables.

## Operability and security

Structured logs, correlation IDs, metrics, traces, and audit records are platform requirements.
Secrets enter through environment variables locally and a managed secret store in deployed
environments. Production readiness will add dependency probes, rate limits, secure headers,
encryption/key policy, backups, restore tests, data retention, and SLO-based alerting.

## Planned capability modules

- portfolio and project 360
- schedules, milestones, progress, and critical-path intelligence
- causal evidence and dependency management
- risk registers, propagation, and scenario simulation
- supply chain, procurement, contracts, and commercial events
- document ingestion, extraction, classification, and retrieval
- graph analytics and GraphRAG
- governed AI copilot, tools, agents, and human approvals
- notifications, audit, administration, and reporting

These are boundaries, not committed service deployments. Extraction will require measured evidence
such as incompatible scaling, isolation, or ownership needs.
