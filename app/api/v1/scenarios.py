from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.data.synthetic_scenarios import (
    SUPPORTED_DISEASES,
    SUPPORTED_GEOGRAPHIES,
    SYNTHETIC_DATA_NOTICE,
)
from app.schemas.epidemiology import (
    ScenarioListResponse,
    ScenarioResponse,
)
from app.services.scenario_service import get_scenario


router = APIRouter(
    prefix="/data",
    tags=["epidemiology data"],
)


@router.get(
    "/scenario",
    response_model=ScenarioResponse,
)
def scenario(
    disease: str = Query(..., min_length=1),
    geography: str = Query(..., min_length=1),
):
    result = get_scenario(
        disease=disease,
        geography=geography,
    )

    response = {
        "status": result.status,
        "provider": result.provider,
        "mode": result.mode,
        "disease": result.disease,
        "geography": result.geography,
        "data_status": (
            "SYNTHETIC DATA"
            if result.scenario is not None
            else "DATA UNAVAILABLE"
        ),
        "notice": SYNTHETIC_DATA_NOTICE,
        "scenario": result.scenario,
        "message": result.message,
    }

    if result.status != "AVAILABLE":
        return JSONResponse(
            status_code=404,
            content=response,
        )

    return response


@router.get(
    "/scenario-options",
    response_model=ScenarioListResponse,
)
def scenario_options() -> ScenarioListResponse:
    return ScenarioListResponse(
        diseases=list(SUPPORTED_DISEASES),
        geographies=list(SUPPORTED_GEOGRAPHIES),
        notice=SYNTHETIC_DATA_NOTICE,
    )