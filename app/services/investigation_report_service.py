from app.schemas.investigation import InvestigationResult
from app.schemas.investigation_report import InvestigationReport


def generate_investigation_report(
    result: InvestigationResult,
) -> InvestigationReport:
    """
    Convert a completed investigation result into a concise
    investigator-facing report.

    This service is deterministic for the MVP.
    It does not introduce new epidemiological evidence,
    scores, or autonomous decisions.
    """

    if result.overall_signal == "ELEVATED":
        summary = (
            f"The investigation identified an elevated {result.disease} "
            f"signal in {result.geography}. Multiple available synthetic "
            "evidence sources support further investigation."
        )
    elif result.overall_signal == "MODERATE":
        summary = (
            f"The investigation identified a moderate {result.disease} "
            f"signal in {result.geography}. The available evidence "
            "supports continued monitoring and human review."
        )
    elif result.overall_signal == "ANOMALY":
        summary = (
            f"The surveillance series shows an anomalous {result.disease} "
            f"signal in {result.geography}. Further investigation is required "
            "to determine whether the signal represents a meaningful event."
        )
    else:
        summary = (
            f"No elevated overall signal was identified for {result.disease} "
            f"in {result.geography} using the available demonstration data."
        )

    supporting_evidence: list[str] = []

    if result.anomaly.status == "ANOMALY":
        supporting_evidence.append(
            "The surveillance series is above the configured baseline "
            "anomaly threshold."
        )

    for item in result.evidence.evidence:
        if item.signal == "ELEVATED":
            supporting_evidence.append(
                f"{item.source} shows an elevated signal."
            )

    elevated_geographies = [
        item
        for item in result.evidence.geographic_evidence
        if item.signal == "ELEVATED"
    ]

    if elevated_geographies:
        supporting_evidence.append(
            f"{len(elevated_geographies)} geographic areas show elevated signals."
        )

    if result.forecast.risk_level in {"ELEVATED", "MODERATE"}:
        supporting_evidence.append(
            f"The numerical forecast indicates {result.forecast.risk_level.lower()} "
            "projected risk."
        )

    investigation_priorities: list[str] = [
        "Verify the signal against available primary surveillance records.",
        "Review affected geographic areas for clustering or spread.",
        "Review hospital and laboratory signals for corroborating evidence.",
        "Assess relevant environmental or contextual factors.",
    ]

    if result.forecast.risk_level in {"ELEVATED", "MODERATE"}:
        investigation_priorities.append(
            "Review the forecast trend and monitor changes over the forecast horizon."
        )

    return InvestigationReport(
        disease=result.disease,
        geography=result.geography,
        summary=summary,
        key_findings=result.key_findings,
        investigation_priorities=investigation_priorities,
        supporting_evidence=supporting_evidence,
        uncertainty=result.uncertainty,
        data_status=result.data_status,
        notice=result.notice,
        human_review_required=result.human_review_required,
    )