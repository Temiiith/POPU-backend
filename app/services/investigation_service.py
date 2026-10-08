from app.services.anomaly_service import detect_anomaly
from app.services.evidence_service import assess_evidence
from app.services.forecast_service import forecast_disease_risk
from app.services.risk_service import assess_risk
from app.schemas.investigation import InvestigationResult
from app.services.risk_fusion_service import assess_integrated_risk


def investigate(
    disease: str,
    geography: str,
    forecast_horizon_days: int = 7,
) -> InvestigationResult | None:
    anomaly = detect_anomaly(
        disease=disease,
        geography=geography,
    )

    evidence = assess_evidence(
        disease=disease,
        geography=geography,
    )

    forecast = forecast_disease_risk(
        disease=disease,
        geography=geography,
        horizon_days=forecast_horizon_days,
    )

    risk = assess_risk(
        disease=disease,
        geography=geography,
    )

    integrated_risk = assess_integrated_risk(
        disease=disease,
        geography=geography,
        forecast_horizon_days=forecast_horizon_days,
    )

    if (
        anomaly is None
        or evidence is None
        or forecast is None
        or risk is None
        or integrated_risk is None
    ):
        return None

    key_findings: list[str] = []

    if anomaly.status == "ANOMALY":
        key_findings.append(
            "The surveillance series shows an anomaly relative to the configured baseline."
        )

    if evidence.elevated_signal_count > 0:
        key_findings.append(
            f"{evidence.elevated_signal_count} evidence sources show elevated signals."
        )

    elevated_geographies = [
        item
        for item in evidence.geographic_evidence
        if item.signal == "ELEVATED"
    ]

    if elevated_geographies:
        key_findings.append(
            f"{len(elevated_geographies)} geographic areas show elevated signals."
        )

    if forecast.risk_level == "ELEVATED":
        key_findings.append(
            "The numerical forecast indicates elevated projected risk."
        )
    elif forecast.risk_level == "MODERATE":
        key_findings.append(
            "The numerical forecast indicates moderate projected risk."
        )
    else:
        key_findings.append(
            "The numerical forecast remains below the configured moderate-risk threshold."
        )

    if risk.risk_level == "ELEVATED":
        overall_signal = "ELEVATED"
    elif risk.risk_level == "MODERATE":
        overall_signal = "MODERATE"
    elif anomaly.status == "ANOMALY":
        overall_signal = "ANOMALY"
    else:
        overall_signal = "LOW"

    return InvestigationResult(
        disease=disease,
        geography=geography,
        anomaly=anomaly,
        evidence=evidence,
        forecast=forecast,
        risk=risk,
        integrated_risk=integrated_risk,
        overall_signal=overall_signal,
        key_findings=key_findings,
        data_status="SYNTHETIC DATA",
        notice=(
            "SYNTHETIC DEMONSTRATION DATA - "
            "NOT FOR OFFICIAL CLINICAL ACTION"
        ),
        uncertainty=[
            "All investigation inputs are synthetic demonstration data.",
            "An anomaly does not by itself confirm an outbreak.",
            "Risk assessment is based on a transparent demonstration scoring method.",
            "The forecast uses a simple baseline trend and is not a validated epidemiological forecasting model.",
            "Investigation findings require human review.",
        ],
        human_review_required=True,
    )