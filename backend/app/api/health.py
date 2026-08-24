from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["platform"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        environment=settings.environment,
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ReadinessResponse}},
)
async def readiness(request: Request) -> ReadinessResponse | JSONResponse:
    ready = bool(getattr(request.app.state, "ready", False))
    payload = ReadinessResponse(
        status="ready" if ready else "not_ready",
        checks={"application": "up" if ready else "starting"},
    )
    if not ready:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=payload.model_dump(),
        )
    return payload
