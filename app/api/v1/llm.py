from fastapi import APIRouter, HTTPException

from app.agents.popu_agent import run_popu_agent
from app.schemas.agent import AgentIntent
from app.schemas.data_availability import DataAvailabilityResponse
from app.schemas.investigation import InvestigationResult
from app.schemas.llm import LLMInterpretation
from app.schemas.llm_request import LLMInterpretationRequest
from app.services.llm.orchestrator import LLMOrchestrator
from app.services.llm.prompt_builder import build_investigation_prompt


router = APIRouter(
    prefix="/llm",
    tags=["llm"],
)


@router.post(
    "/interpret",
    response_model=LLMInterpretation,
)
def interpret_investigation(
    payload: LLMInterpretationRequest,
) -> LLMInterpretation:
    result = run_popu_agent(
        request=payload.request,
        forecast_horizon_days=payload.forecast_horizon_days,
    )

    if isinstance(result, AgentIntent):
        raise HTTPException(
            status_code=400,
            detail="The request could not be interpreted as a supported epidemiological investigation.",
        )

    if isinstance(result, DataAvailabilityResponse):
        raise HTTPException(
            status_code=404,
            detail=result.message,
        )

    if not isinstance(result, InvestigationResult):
        raise HTTPException(
            status_code=500,
            detail="Unexpected investigation result.",
        )

    prompt = build_investigation_prompt(result)

    try:
        llm_result = LLMOrchestrator().generate(prompt)
    except Exception:
        return LLMInterpretation(
            provider="popu_deterministic",
            model="deterministic_investigation_engine",
            fallback_used=True,
            interpretation=(
                "POPU completed the epidemiological investigation using "
                "its deterministic analysis engines. The configured LLM "
                "provider was temporarily unavailable, so no AI-generated "
                "interpretation was produced."
            ),
            uncertainty=[
                *result.uncertainty,
                "AI interpretation was unavailable for this request.",
                "The displayed findings are deterministic POPU analysis outputs, not an LLM interpretation.",
            ],
            human_review_required=True,
        )
    return LLMInterpretation(
        provider=llm_result.provider,
        model=llm_result.model,
        fallback_used=llm_result.fallback_used,
        interpretation=llm_result.text,
        uncertainty=result.uncertainty,
        human_review_required=True,
    )
