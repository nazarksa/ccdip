# Architecture Decision Log

## ADR-001: Start with a modular monolith

**Status:** Accepted

Deploy the core API as one application while enforcing capability boundaries in code. This keeps
transactions, local development, and operations simple. A module may be extracted only when
measured scaling, resilience, security, ownership, or deployment constraints justify it.

## ADR-002: PostgreSQL is authoritative

**Status:** Accepted

Transactional entities and source metadata live in PostgreSQL. Neo4j stores graph projections,
Redis stores ephemeral data, object storage stores binary content, and pgvector supports semantic
indexes close to governed metadata. Derived stores must be rebuildable.

## ADR-003: Async at I/O boundaries

**Status:** Accepted

FastAPI routes and database clients use async interfaces where operations are I/O-bound. CPU-heavy
analytics and long-running ingestion do not execute in request handlers; they move to workers.

## ADR-004: Typed configuration and secret injection

**Status:** Accepted

Pydantic Settings validates runtime configuration. Local values may come from `.env`; deployed
secrets come from the hosting platform or secret manager. Secrets are never committed.

## ADR-005: React server-state ownership

**Status:** Accepted

TanStack Query owns server state and caching. Router state and local React state remain preferred
for navigation and component concerns. Zustand is used only for cross-component client workflows
that do not fit those models.

## ADR-006: AI and graph capabilities remain unimplemented

**Status:** Accepted

The repository reserves boundaries but introduces no agents, prompts, graph algorithms, causal
logic, schedule engine, or risk simulation in this phase. Future AI output must include provenance,
evaluation, authorization, cost controls, and human-review policy.

## Pending decisions

- enterprise identity provider, token validation, and project-scoped RBAC model
- background job technology and transactional outbox implementation
- tenancy/isolation model and Saudi data-residency controls
- graph projection schema and consistency/replay protocol
- observability platform and audit retention policy
- document malware scanning, classification, and lifecycle policy
- deployment topology, availability targets, backup, and disaster recovery
