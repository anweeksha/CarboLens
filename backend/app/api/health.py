"""Health endpoints. Database checks live in app.database.session."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.database.session import check_connection
from app.schemas.health import DatabaseHealthResponse, HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="healthy", service="CarbonLens API")


@router.get("/health/db", response_model=DatabaseHealthResponse)
def get_database_health() -> DatabaseHealthResponse | JSONResponse:
    try:
        check_connection()
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"},
        )
    return DatabaseHealthResponse(status="healthy", database="connected")
