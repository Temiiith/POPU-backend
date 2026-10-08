from app.data_providers.registry import get_data_provider
from app.schemas.anomaly import AnomalyResult


DEFAULT_ELEVATED_THRESHOLD_PERCENT = 25.0
DEFAULT_ANOMALY_THRESHOLD_PERCENT = 50.0


def detect_anomaly(
    disease: str,
    geography: str,
    elevated_threshold_percent: float = DEFAULT_ELEVATED_THRESHOLD_PERCENT,
    anomaly_threshold_percent: float = DEFAULT_ANOMALY_THRESHOLD_PERCENT,
) -> AnomalyResult | None:
    provider = get_data_provider("synthetic_demo")

    result = provider.get_scenario(
        disease=disease,
        geography=geography,
    )

    if result.scenario is None:
        return None

    surveillance = result.scenario["surveillance"]

    baseline_value = float(
        surveillance["weekly_baseline_cases"]
    )

    observed_value = float(
        surveillance["recent_week_cases"]
    )

    if baseline_value <= 0:
        return None

    absolute_deviation = observed_value - baseline_value

    percent_deviation = (
        absolute_deviation / baseline_value
    ) * 100

    if percent_deviation >= anomaly_threshold_percent:
        status = "ANOMALY"
    elif percent_deviation >= elevated_threshold_percent:
        status = "ELEVATED"
    else:
        status = "NORMAL"

    uncertainty = [
        "All input values are synthetic demonstration data.",
        "Thresholds are demonstration parameters, not clinical or public-health standards.",
        "Anomaly classification does not confirm an outbreak.",
    ]

    return AnomalyResult(
        status=status,
        disease=result.disease,
        geography=result.geography,
        data_status="SYNTHETIC DATA",
        notice=(
            "SYNTHETIC DEMONSTRATION DATA - "
            "NOT FOR OFFICIAL CLINICAL ACTION"
        ),
        baseline_value=baseline_value,
        observed_value=observed_value,
        absolute_deviation=round(absolute_deviation, 2),
        percent_deviation=round(percent_deviation, 2),
        threshold_percent=anomaly_threshold_percent,
        method="baseline_percentage_deviation",
        model_output=(
            "Recent reported cases are above the configured "
            "demonstration baseline threshold."
            if status != "NORMAL"
            else
            "Recent reported cases are within the configured "
            "demonstration baseline range."
        ),
        uncertainty=uncertainty,
        human_review_required=True,
    )