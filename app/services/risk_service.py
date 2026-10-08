from app.data_providers.registry import get_data_provider
from app.schemas.risk import RiskAssessment


def _calculate_risk_score(
    elevated_signals: int,
    moderate_signals: int,
    geographic_elevated_signals: int,
) -> float:
    """
    Calculate a deterministic demonstration risk score.

    This is a transparent rule-based score for the synthetic MVP.
    It is not a validated epidemiological risk model.
    """

    score = (
        elevated_signals * 20
        + moderate_signals * 10
        + geographic_elevated_signals * 10
    )

    return round(min(100.0, float(score)), 2)


def _risk_level(risk_score: float) -> str:
    if risk_score >= 60:
        return "ELEVATED"

    if risk_score >= 30:
        return "MODERATE"

    return "LOW"


def assess_risk(
    disease: str,
    geography: str,
) -> RiskAssessment | None:
    provider = get_data_provider("synthetic_demo")

    result = provider.get_scenario(
        disease=disease,
        geography=geography,
    )

    if result.scenario is None:
        return None

    scenario = result.scenario

    surveillance = scenario["surveillance"]
    hospital = scenario["hospital"]
    laboratory = scenario["laboratory"]
    environmental = scenario["environmental"]
    geographic_signals = scenario["geographic_signals"]

    evidence_signals = [
        surveillance,
        hospital,
        laboratory,
        environmental,
    ]

    elevated_signals = 0
    moderate_signals = 0
    stable_signals = 0

    for signal_source in evidence_signals:
        signal = signal_source.get("signal")

        if signal == "elevated":
            elevated_signals += 1
        elif signal == "moderate":
            moderate_signals += 1
        elif signal == "stable":
            stable_signals += 1

    geographic_elevated_signals = sum(
        1
        for signal in geographic_signals
        if signal.get("signal") == "elevated"
    )

    risk_score = _calculate_risk_score(
        elevated_signals=elevated_signals,
        moderate_signals=moderate_signals,
        geographic_elevated_signals=geographic_elevated_signals,
    )

    risk_level = _risk_level(risk_score)

    contributing_factors: list[str] = []

    if surveillance.get("case_change_percent", 0) > 0:
        contributing_factors.append(
            "Reported surveillance cases are above the configured baseline."
        )

    if hospital.get("signal") == "elevated":
        contributing_factors.append(
            "Hospital syndrome reporting contains an elevated signal."
        )

    if laboratory.get("signal") == "elevated":
        contributing_factors.append(
            "Laboratory reporting contains an elevated signal."
        )

    if environmental.get("signal") == "elevated":
        contributing_factors.append(
            "Environmental reporting contains an elevated signal."
        )

    if geographic_elevated_signals > 0:
        contributing_factors.append(
            f"{geographic_elevated_signals} geographic areas show elevated signals."
        )

    return RiskAssessment(
        disease=result.disease,
        geography=result.geography,
        risk_level=risk_level,
        risk_score=risk_score,
        evidence_signal_count=len(evidence_signals),
        elevated_signal_count=elevated_signals,
        moderate_signal_count=moderate_signals,
        stable_signal_count=stable_signals,
        contributing_factors=contributing_factors,
        data_status="SYNTHETIC DATA",
        notice=(
            "SYNTHETIC DEMONSTRATION DATA - "
            "NOT FOR OFFICIAL CLINICAL ACTION"
        ),
        uncertainty=[
            "All inputs are synthetic demonstration data.",
            "The risk score is a transparent rule-based demonstration score.",
            "The scoring method has not been clinically or epidemiologically validated.",
            "An elevated risk score does not confirm an outbreak.",
            "Risk assessment requires human review.",
        ],
        human_review_required=True,
    )