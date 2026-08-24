from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Own process-level resources and expose application readiness."""

    app.state.ready = True
    try:
        yield
    finally:
        app.state.ready = False
