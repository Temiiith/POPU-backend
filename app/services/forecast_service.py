from statistics import mean

from app.data_providers.registry import get_data_provider
from app.schemas.forecast import ForecastResult


DEFAULT_FORECAST_HORIZON_DAYS = 7


def _calculate_trend(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0

    differences = [
        values[index] - values[index - 1]
        for index in range(1, len(values))
    ]

    return mean(differences)


def _calculate_risk_score(
    baseline: float,
    forecast_values: list[float],
) -> float:
    if baseline <= 0 or not forecast_values:
        return 0.0

    peak_forecast = max(forecast_values)

    score = (
        (peak_forecast - baseline)
        / baseline
    ) * 100

    return round(
        max(0.0, min(100.0, score)),
        2,
    )


def _risk_level(risk_score: float) -> str:
    if risk_score >= 50:
        return "ELEVATED"

    if risk_score >= 25:
        return "MODERATE"

    return "LOW"


def forecast_disease_risk(
    disease: str,
    geography: str,
    horizon_days: int = DEFAULT_FORECAST_HORIZON_DAYS,
) -> ForecastResult | None:
    if horizon_days < 1:
        return None

    provider = get_data_provider("synthetic_demo")

    result = provider.get_scenario(
        disease=disease,
        geography=geography,
    )

    if result.scenario is None:
        return None

    surveillance = result.scenario["surveillance"]

    daily_cases = surveillance.get("daily_cases", [])

    if not daily_cases:
        return None

    values = [
        float(value)
        for value in daily_cases
    ]

    baseline = float(
        surveillance["weekly_baseline_cases"]
    )

    trend = _calculate_trend(values)

    last_value = values[-1]

    predicted_values = []

    for day in range(1, horizon_days + 1):
        prediction = max(
            0.0,
            last_value + (trend * day),
        )

        predicted_values.append(
            round(prediction, 2)
        )

    risk_score = _calculate_risk_score(
        baseline=baseline,
        forecast_values=predicted_values,
    )

    risk_level = _risk_level(
        risk_score
    )

    confidence_interval = []

    uncertainty_margin = max(
        1.0,
        abs(trend) * 2,
    )

    for prediction in predicted_values:
        confidence_interval.append(
            {
                "lower": round(
                    max(
                        0.0,
                        prediction - uncertainty_margin,
                    ),
                    2,
                ),
                "upper": round(
                    prediction + uncertainty_margin,
                    2,
                ),
            }
        )

    return ForecastResult(
        disease=result.disease,
        geography=result.geography,
        forecast_horizon_days=horizon_days,
        predicted_values=predicted_values,
        risk_level=risk_level,
        risk_score=risk_score,
        confidence_interval=confidence_interval,
        model="baseline_trend_forecast",
        model_version="0.1.0",
        data_status="SYNTHETIC DATA",
        notice=(
            "SYNTHETIC DEMONSTRATION DATA - "
            "NOT FOR OFFICIAL CLINICAL ACTION"
        ),
        uncertainty=[
            "All input values are synthetic demonstration data.",
            "This forecast uses a simple baseline trend and is not a validated epidemiological forecasting model.",
            "Confidence intervals are demonstration estimates.",
            "Forecast output does not confirm an outbreak.",
        ],
        human_review_required=True,
    )