
from fastapi import APIRouter, HTTPException

from app.schemas.data_availability import DataAvailabilityResponse
from app.agents.popu_agent import run_popu_agent
from app.schemas.agent import AgentIntent
from app.schemas.agent_request import AgentRequest
from app.schemas.investigation import InvestigationResult
from app.schemas.investigation_report import InvestigationReport
from app.services.investigation_report_service import (
    generate_investigation_report,
)


router = APIRouter(
    prefix="/agent",
    tags=["agent"],
)


@router.post(
    "/investigate",
    response_model=InvestigationResult | AgentIntent | DataAvailabilityResponse,
)
def investigate_with_agent(
    payload: AgentRequest,
) -> InvestigationResult | AgentIntent | DataAvailabilityResponse:
    result = run_popu_agent(
        request=payload.request,
        forecast_horizon_days=payload.forecast_horizon_days,
    )

    if isinstance(result, DataAvailabilityResponse):
        raise HTTPException(
            status_code=404,
            detail=result.message,
        )

    if isinstance(result, AgentIntent):
        if (
            result.intent == "INVESTIGATE"
            and result.disease is not None
            and result.geography is not None
        ):
            raise HTTPException(
                status_code=404,
                detail=(
                    "No investigation scenario is available "
                    "for the requested disease and geography."
                ),
            )

    return result


@router.post(
    "/investigate/report",
    response_model=InvestigationReport,
)
def generate_agent_investigation_report(
    payload: AgentRequest,
) -> InvestigationReport:
    result = run_popu_agent(
        request=payload.request,
        forecast_horizon_days=payload.forecast_horizon_days,
    )

    if isinstance(result, DataAvailabilityResponse):
        raise HTTPException(
            status_code=404,
            detail=result.message,
        )

    if isinstance(result, AgentIntent):
        if (
            result.intent == "INVESTIGATE"
            and result.disease is not None
            and result.geography is not None
        ):
            raise HTTPException(
                status_code=404,
                detail=(
                    "No investigation scenario is available "
                    "for the requested disease and geography."
                ),
            )

        raise HTTPException(
            status_code=400,
            detail=(
                "The request could not be interpreted as "
                "a supported epidemiological investigation."
            ),
        )

    return generate_investigation_report(result)