# Construction Causality & Dependency Intelligence Platform

Production-oriented foundation for a Saudi construction and giga-project intelligence platform.
The repository currently contains architecture, runtime scaffolding, health endpoints, and local
development infrastructure only. It intentionally contains no simulated business functionality.

## Repository

- `backend/` — FastAPI modular monolith, persistence foundations, migrations, and tests
- `frontend/` — React and TypeScript enterprise application shell
- `infra/` — local service initialization and future deployment assets
- `docs/` — architecture, decision log, and development guidance
- `scripts/` — repeatable operational scripts
- `tests/` — cross-service and end-to-end tests

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Node.js 24+ and npm
- Docker Desktop with Docker Compose

## Quick start

PowerShell:

```powershell
Copy-Item .env.example .env
uv sync --all-groups
npm --prefix frontend ci
docker compose up -d postgres neo4j redis minio
```

Start the API and web application in separate terminals:

```powershell
uv run --package ccdip-backend uvicorn app.main:app --app-dir backend --reload
npm --prefix frontend run dev
```

Open:

- Frontend: http://localhost:5173
- API documentation: http://localhost:8000/docs
- Liveness: http://localhost:8000/health
- Readiness: http://localhost:8000/ready
- Neo4j Browser: http://localhost:7474
- MinIO Console: http://localhost:9001

## Quality checks

```powershell
uv run --package ccdip-backend pytest backend/tests
uv run --package ccdip-backend ruff check backend
uv run --package ccdip-backend mypy backend/app
npm --prefix frontend run lint
npm --prefix frontend run build
docker compose config --quiet
```

Application images are opt-in:

```powershell
docker compose --profile application up --build
```

See `docs/DEVELOPMENT.md` for operating details and `docs/ARCHITECTURE.md` for boundaries.
