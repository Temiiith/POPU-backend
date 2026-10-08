from datetime import datetime, timezone

from app.data.synthetic_scenarios import SYNTHETIC_SCENARIOS
from app.schemas.signal import SignalResult
from app.services.anomaly_service import detect_anomaly
from app.services.evidence_service import assess_evidence
from app.services.forecast_service import forecast_disease_risk
from app.services.risk_fusion_service import assess_integrated_risk


SIGNAL_FORECAST_HORIZON_DAYS = 14


def _forecast_direction(
    predicted_values: list[float],
) -> str:
    if len(predicted_values) < 2:
        return "STABLE"

    first_value = predicted_values[0]
    last_value = predicted_values[-1]

    if last_value > first_value:
        return "INCREASING"

    if last_value < first_value:
        return "DECREASING"

    return "STABLE"


def generate_signal(
    disease: str,
    geography: str,
) -> SignalResult | None:
    anomaly = detect_anomaly(
        disease=disease,
        geography=geography,
    )

    if anomaly is None:
        return None

    if anomaly.status == "NORMAL":
        return None

    scenario = SYNTHETIC_SCENARIOS.get(
        disease.strip().lower(),
        {},
    ).get(
        geography.strip()
    )

    if scenario is None:
        return None

    evidence_assessment = assess_evidence(
        disease=disease,
        geography=geography,
    )

    if evidence_assessment is None:
        return None

    integrated_risk = assess_integrated_risk(
        disease=disease,
        geography=geography,
        forecast_horizon_days=SIGNAL_FORECAST_HORIZON_DAYS,
    )

    forecast = forecast_disease_risk(
        disease=disease,
        geography=geography,
        horizon_days=SIGNAL_FORECAST_HORIZON_DAYS,
    )

    if integrated_risk is None or forecast is None:
        return None

    supporting_sources = [
        item.source
        for item in evidence_assessment.evidence
        if item.signal in {"ELEVATED", "MODERATE"}
    ]

    geographic_signal_count = sum(
        1
        for item in evidence_assessment.geographic_evidence
        if item.signal in {"ELEVATED", "MODERATE"}
    )

    severity = (
        "HIGH"
        if anomaly.status == "ANOMALY"
        else "MODERATE"
    )

    signal_id = (
        f"SIG-{disease.upper().replace(' ', '_')}-"
        f"{geography.upper().replace(' ', '_')}"
    )

    return SignalResult(
        signal_id=signal_id,
        disease=anomaly.disease,
        geography=anomaly.geography,
        status=anomaly.status,
        severity=severity,
        detected_at=datetime.now(timezone.utc),
        baseline_value=anomaly.baseline_value,
        observed_value=anomaly.observed_value,
        percent_deviation=anomaly.percent_deviation,
        detection_method=anomaly.method,
        source="POPU Synthetic Scenario Provider",
        summary=(
            f"{anomaly.disease} in {anomaly.geography} shows an "
            f"{anomaly.status.lower()} signal relative to the configured "
            f"surveillance baseline."
        ),
        supporting_sources=supporting_sources,
        elevated_source_count=(
            evidence_assessment.elevated_signal_count
        ),
        moderate_source_count=(
            evidence_assessment.moderate_signal_count
        ),
        geographic_signal_count=geographic_signal_count,
        risk_level=integrated_risk.risk_level,
        risk_score=integrated_risk.risk_score,
        forecast_risk_level=forecast.risk_level,
        forecast_risk_score=forecast.risk_score,
        forecast_horizon_days=forecast.forecast_horizon_days,
        forecast_direction=_forecast_direction(
            forecast.predicted_values
        ),
        data_status=scenario["data_status"],
        notice=scenario["notice"],
        human_review_required=True,
        uncertainty=(
            anomaly.uncertainty
            + evidence_assessment.uncertainty
            + integrated_risk.uncertainty
            + forecast.uncertainty
        ),
    )


def scan_all_signals() -> list[SignalResult]:
    signals: list[SignalResult] = []

    for disease, disease_scenarios in SYNTHETIC_SCENARIOS.items():
        for geography in disease_scenarios:
            signal = generate_signal(
                disease=disease,
                geography=geography,
            )

            if signal is not None:
                signals.append(signal)

    return signals