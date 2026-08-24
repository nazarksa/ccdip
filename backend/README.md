# Backend

FastAPI-based modular monolith for the CCDI platform.

## Run

From the repository root:

```powershell
uv sync --all-groups
uv run --package ccdip-backend uvicorn app.main:app --app-dir backend --reload
```

The application exposes `/health`, `/ready`, and OpenAPI documentation at `/docs`.

## Boundaries

- `api`, `schemas`: transport layer
- `services`: application use cases and transaction coordination
- `domain` and capability packages: business policy
- `repositories`, `db`, `models`, `graph`: persistence adapters
- `core`, `config`, `security`, `audit`: platform concerns
- `events`, `workers`, `workflows`: asynchronous coordination

Capability packages must not import from the API layer. Infrastructure details should stay out of
domain policy. Cross-capability writes should be coordinated by an application service and later
published through a transactional outbox where asynchronous delivery is required.

## Database migrations

```powershell
uv run --package ccdip-backend alembic -c backend/alembic.ini revision --autogenerate -m "change"
uv run --package ccdip-backend alembic -c backend/alembic.ini upgrade head
```

Import every model from `app.models` before generating migrations so Alembic can discover metadata.

Create the transactional schema and load the idempotent development dataset:

```powershell
uv run --package ccdip-backend alembic -c backend/alembic.ini upgrade head
uv run --package ccdip-backend python -m app.db.seed
```

The CRUD endpoints under `/api/v1` require an `X-Tenant-ID` UUID header. Resources currently
exposed are projects, activities, suppliers, materials, contracts, risks, delays, and documents.
Repository queries always include this tenant boundary.

## Tests

Tests use PostgreSQL rather than SQLite. Start the Compose PostgreSQL service, then run:

```powershell
docker compose up -d postgres
uv run --package ccdip-backend pytest
```

The suite derives an isolated `ccdip_test` database from `DATABASE_URL`. Set `TEST_DATABASE_URL`
when the test database uses different credentials. The configured database user must be allowed to
create and drop the test database.
