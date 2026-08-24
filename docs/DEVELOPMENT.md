# Development

## Bootstrap

From the repository root on Windows PowerShell:

```powershell
Copy-Item .env.example .env
uv sync --all-groups
npm --prefix frontend ci
docker compose up -d postgres neo4j redis minio
docker compose ps
```

Change local passwords in `.env`. The committed defaults are development-only and must never be
used outside a developer machine.

## Run

API terminal:

```powershell
uv run --package ccdip-backend uvicorn app.main:app --app-dir backend --reload
```

Frontend terminal:

```powershell
npm --prefix frontend run dev
```

Stop infrastructure without deleting data using `docker compose stop`. Use `docker compose down -v`
only when local data can be discarded.

## Verification

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/ready
uv run --package ccdip-backend pytest backend/tests
uv run --package ccdip-backend ruff check backend
uv run --package ccdip-backend mypy backend/app
npm --prefix frontend run lint
npm --prefix frontend run build
docker compose config --quiet
```

## Database changes

Start PostgreSQL, import model modules in `app.models`, then generate and inspect a migration:

```powershell
uv run --package ccdip-backend alembic -c backend/alembic.ini revision --autogenerate -m "change"
uv run --package ccdip-backend alembic -c backend/alembic.ini upgrade head
```

Never edit an already-applied migration. Data migrations must be safe to retry or have an explicit
recovery procedure.

## Module rules

- Put business language and invariants in the owning capability package.
- Keep HTTP and storage details outside domain policy.
- Do not access another capability's tables directly from route handlers.
- Avoid generic base repositories and speculative abstractions.
- Record consequential architecture decisions in `DECISIONS.md`.
- Add tests with every behavior; place cross-service tests under root `tests`.
- Keep AI, graph analysis, schedule calculation, and risk simulation out until their designs and
  acceptance criteria are approved.

## CI

GitHub Actions checks backend formatting/linting, typing, and tests; frontend lint and production
build; Compose validity; and both application container builds. CI uses lockfiles for repeatability.
