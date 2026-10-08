from app.schemas.investigation import InvestigationResult
from app.services.investigation_service import investigate


def run_investigation_agent(
    disease: str,
    geography: str,
    forecast_horizon_days: int = 7,
) -> InvestigationResult | None:
    """
    Run the POPU epidemiological investigation workflow.

    This first agent implementation is deterministic and uses
    the validated investigation service as its analysis engine.

    It does not make autonomous public-health decisions.
    Human review remains required.
    """

    if not disease.strip():
        return None

    if not geography.strip():
        return None

    if forecast_horizon_days < 1 or forecast_horizon_days > 30:
        return None

    result = investigate(
        disease=disease.strip(),
        geography=geography.strip(),
        forecast_horizon_days=forecast_horizon_days,
    )

    if result is None:
        return None

    return result