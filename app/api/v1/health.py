from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["system"])


@router.get("/health")
def health() -> dict:
    return {
        "status": "healthy",
        "service": "popu-api",
        "version": settings.app_version,
        "environment": settings.environment,
        "data_mode": settings.data_mode,
        "production_data_connected": False,
        "synthetic_notice": (
            "SYNTHETIC DEMONSTRATION DATA - NOT FOR OFFICIAL CLINICAL ACTION"
        ),
    }
