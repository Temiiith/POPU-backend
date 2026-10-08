from app.schemas.data_availability import DataAvailabilityResponse
from app.agents.intent_agent import parse_investigation_request
from app.schemas.investigation import InvestigationResult
from app.schemas.agent import AgentIntent
from app.services.investigation_service import investigate


def run_popu_agent(
    request: str,
    forecast_horizon_days: int = 7,
) -> InvestigationResult | AgentIntent | DataAvailabilityResponse:
    """
    Run the POPU natural-language investigation workflow.

    Flow:
        User request
        -> Intent parsing
        -> Investigation workflow
        -> Structured result

    The agent is deterministic in the MVP.
    It does not use an LLM and does not make autonomous
    public-health decisions.
    """

    intent = parse_investigation_request(request)

    if intent.intent == "UNKNOWN":
        return intent

    if intent.disease is None:
        return intent

    if intent.geography is None:
        return intent

    if forecast_horizon_days < 1 or forecast_horizon_days > 30:
        return AgentIntent(
            intent="UNKNOWN",
            original_request=request.strip(),
        )

    result = investigate(
        disease=intent.disease,
        geography=intent.geography,
        forecast_horizon_days=forecast_horizon_days,
    )

    if result is None:
        return DataAvailabilityResponse(
            status="SOURCE_NOT_CONFIGURED",
            disease=intent.disease,
            geography=intent.geography,
            provider="POPU Synthetic Scenario Provider",
            message=(
                f"No epidemiological data source or synthetic "
                f"demonstration scenario is currently configured for "
                f"{intent.disease} in {intent.geography}."
            ),
            notice=(
                "POPU supports Nigeria-wide geography, but current "
                "demonstration data coverage varies by disease and geography."
            ),
        )

    return result