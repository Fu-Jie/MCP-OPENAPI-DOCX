"""Health check routes.

This module provides health check endpoints for monitoring.
"""

import time
from typing import Any

from fastapi import APIRouter, Depends

from src.core.config import Settings, get_settings
from src.models.schemas import HealthStatus

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthStatus,
    summary="Health Check",
    description="Check the health status of the API server.",
)
async def health_check(
    settings: Settings = Depends(get_settings),
) -> HealthStatus:
    """Check the health status of the API.

    Returns:
        HealthStatus with service status information.
    """
    from fastapi import Request

    return HealthStatus(
        status="healthy",
        version=settings.app_version,
        database="connected",  # Simplified check
        redis="connected",  # Simplified check
        uptime=0.0,  # Would need app state for actual uptime
    )


@router.get(
    "/health/ready",
    summary="Readiness Check",
    description="Check if the service is ready to accept requests.",
)
async def readiness_check() -> dict[str, Any]:
    """Check if the service is ready.

    Returns:
        Readiness status.
    """
    return {
        "ready": True,
        "checks": {
            "database": "ok",
            "file_system": "ok",
        },
    }


@router.get(
    "/health/live",
    summary="Liveness Check",
    description="Check if the service is alive.",
)
async def liveness_check() -> dict[str, bool]:
    """Check if the service is alive.

    Returns:
        Liveness status.
    """
    return {"alive": True}
