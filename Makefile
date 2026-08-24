.PHONY: install infra-up infra-down backend frontend test lint format build

install:
	uv sync --all-groups
	npm --prefix frontend ci

infra-up:
	docker compose up -d postgres neo4j redis minio

infra-down:
	docker compose down

backend:
	uv run --package ccdip-backend uvicorn app.main:app --app-dir backend --reload

frontend:
	npm --prefix frontend run dev

test:
	uv run --package ccdip-backend pytest backend/tests

lint:
	uv run --package ccdip-backend ruff check backend
	uv run --package ccdip-backend ruff format --check backend
	uv run --package ccdip-backend mypy backend/app
	npm --prefix frontend run lint

format:
	uv run --package ccdip-backend ruff format backend

build:
	docker compose --profile application build
