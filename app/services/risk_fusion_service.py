from app.schemas.risk_fusion import (
    IntegratedRiskAssessment,
    RiskComponent,
)
from app.services.anomaly_service import detect_anomaly
from app.services.evidence_service import assess_evidence
from app.services.forecast_service import forecast_disease_risk


def _risk_level(risk_score: float) -> str:
    if risk_score >= 60:
        return "ELEVATED"

    if risk_score >= 30:
        return "MODERATE"

    return "LOW"


def _geographic_contribution(
    elevated_geographies: int,
) -> float:
    if elevated_geographies <= 0:
        return 0.0

    return min(
        15.0,
        elevated_geographies * 5.0,
    )


def _forecast_contribution(
    forecast_risk_level: str,
) -> float:
    if forecast_risk_level == "ELEVATED":
        return 15.0

    if forecast_risk_level == "MODERATE":
        return 10.0

    return 0.0


def assess_integrated_risk(
    disease: str,
    geography: str,
    forecast_horizon_days: int = 7,
) -> IntegratedRiskAssessment | None:
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

    if (
        anomaly is None
        or evidence is None
        or forecast is None
    ):
        return None

    components: list[RiskComponent] = []

    total_score = 0.0

    # ---------------------------------------------------------
    # Anomaly contribution
    # ---------------------------------------------------------

    anomaly_contribution = (
        25.0
        if anomaly.status == "ANOMALY"
        else 0.0
    )

    total_score += anomaly_contribution

    components.append(
        RiskComponent(
            name="Anomaly",
            signal=anomaly.status,
            contribution=anomaly_contribution,
            explanation=(
                "The observed surveillance value exceeds "
                "the configured anomaly threshold."
                if anomaly.status == "ANOMALY"
                else
                "The observed surveillance value does not "
                "exceed the configured anomaly threshold."
            ),
        )
    )

    # ---------------------------------------------------------
    # Hospital contribution
    # ---------------------------------------------------------

    hospital_evidence = next(
        (
            item
            for item in evidence.evidence
            if item.source == "hospital"
        ),
        None,
    )

    hospital_contribution = (
        10.0
        if hospital_evidence
        and hospital_evidence.signal == "ELEVATED"
        else 0.0
    )

    total_score += hospital_contribution

    components.append(
        RiskComponent(
            name="Hospital",
            signal=(
                hospital_evidence.signal
                if hospital_evidence
                else "UNKNOWN"
            ),
            contribution=hospital_contribution,
            explanation=(
                "Hospital syndrome reporting contains "
                "an elevated signal."
                if hospital_contribution > 0
                else
                "Hospital syndrome reporting does not "
                "currently contribute elevated risk."
            ),
        )
    )

    # ---------------------------------------------------------
    # Laboratory contribution
    # ---------------------------------------------------------

    laboratory_evidence = next(
        (
            item
            for item in evidence.evidence
            if item.source == "laboratory"
        ),
        None,
    )

    laboratory_contribution = (
        10.0
        if laboratory_evidence
        and laboratory_evidence.signal == "ELEVATED"
        else 0.0
    )

    total_score += laboratory_contribution

    components.append(
        RiskComponent(
            name="Laboratory",
            signal=(
                laboratory_evidence.signal
                if laboratory_evidence
                else "UNKNOWN"
            ),
            contribution=laboratory_contribution,
            explanation=(
                "Laboratory reporting contains "
                "an elevated signal."
                if laboratory_contribution > 0
                else
                "Laboratory reporting does not currently "
                "contribute elevated risk."
            ),
        )
    )

    # ---------------------------------------------------------
    # Environmental contribution
    # ---------------------------------------------------------

    environmental_evidence = next(
        (
            item
            for item in evidence.evidence
            if item.source == "environmental"
        ),
        None,
    )

    environmental_contribution = (
        10.0
        if environmental_evidence
        and environmental_evidence.signal == "ELEVATED"
        else 0.0
    )

    total_score += environmental_contribution

    components.append(
        RiskComponent(
            name="Environmental",
            signal=(
                environmental_evidence.signal
                if environmental_evidence
                else "UNKNOWN"
            ),
            contribution=environmental_contribution,
            explanation=(
                "Environmental reporting contains "
                "an elevated signal."
                if environmental_contribution > 0
                else
                "Environmental reporting does not currently "
                "contribute elevated risk."
            ),
        )
    )

    # ---------------------------------------------------------
    # Geographic contribution
    # ---------------------------------------------------------

    elevated_geographies = sum(
        1
        for item in evidence.geographic_evidence
        if item.signal == "ELEVATED"
    )

    geographic_contribution = _geographic_contribution(
        elevated_geographies
    )

    total_score += geographic_contribution

    components.append(
        RiskComponent(
            name="Geographic clustering",
            signal=(
                "ELEVATED"
                if elevated_geographies > 0
                else "STABLE"
            ),
            contribution=geographic_contribution,
            explanation=(
                f"{elevated_geographies} geographic areas "
                "show elevated signals."
                if elevated_geographies > 0
                else
                "No geographic areas currently show "
                "elevated signals."
            ),
        )
    )

    # ---------------------------------------------------------
    # Forecast contribution
    # ---------------------------------------------------------

    forecast_contribution = _forecast_contribution(
        forecast.risk_level
    )

    total_score += forecast_contribution

    components.append(
        RiskComponent(
            name="Forecast",
            signal=forecast.risk_level,
            contribution=forecast_contribution,
            explanation=(
                "The numerical forecast indicates "
                "elevated projected risk."
                if forecast.risk_level == "ELEVATED"
                else
                "The numerical forecast does not indicate "
                "elevated projected risk."
            ),
        )
    )

    risk_score = round(
        min(100.0, total_score),
        2,
    )

    risk_level = _risk_level(risk_score)

    key_factors: list[str] = []

    if anomaly.status == "ANOMALY":
        key_factors.append(
            "Surveillance anomaly detected."
        )

    if hospital_contribution > 0:
        key_factors.append(
            "Elevated hospital syndrome signal."
        )

    if laboratory_contribution > 0:
        key_factors.append(
            "Elevated laboratory signal."
        )

    if environmental_contribution > 0:
        key_factors.append(
            "Elevated environmental signal."
        )

    if elevated_geographies > 0:
        key_factors.append(
            f"{elevated_geographies} geographic areas "
            "show elevated signals."
        )

    if forecast.risk_level == "ELEVATED":
        key_factors.append(
            "Forecast indicates elevated projected risk."
        )

    return IntegratedRiskAssessment(
        disease=disease,
        geography=geography,
        risk_level=risk_level,
        risk_score=risk_score,
        components=components,
        key_factors=key_factors,
        data_status="SYNTHETIC DATA",
        notice=(
            "SYNTHETIC DEMONSTRATION DATA - "
            "NOT FOR OFFICIAL CLINICAL ACTION"
        ),
        uncertainty=[
            "All inputs are synthetic demonstration data.",
            "The integrated score is a transparent demonstration method.",
            "The weighting scheme has not been epidemiologically validated.",
            "An elevated integrated risk score does not confirm an outbreak.",
            "Forecast and anomaly outputs have their own model limitations.",
            "Human review is required before any public-health action.",
        ],
        human_review_required=True,
    )