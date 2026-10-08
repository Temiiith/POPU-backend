from app.data_providers.registry import get_data_provider
from app.schemas.evidence import (
    EvidenceAssessment,
    EvidenceItem,
    GeographicEvidence,
)


def _signal_value(value: str | None) -> str:
    if value is None:
        return "UNKNOWN"

    normalized = value.strip().lower()

    if normalized == "elevated":
        return "ELEVATED"

    if normalized == "moderate":
        return "MODERATE"

    if normalized == "stable":
        return "STABLE"

    return "UNKNOWN"


def _geographic_deviation(
    cases: float,
    baseline_cases: float,
) -> float:
    if baseline_cases <= 0:
        return 0.0

    return round(
        ((cases - baseline_cases) / baseline_cases) * 100,
        2,
    )


def assess_evidence(
    disease: str,
    geography: str,
) -> EvidenceAssessment | None:
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

    evidence: list[EvidenceItem] = []

    surveillance_change = float(
        surveillance["case_change_percent"]
    )

    evidence.append(
        EvidenceItem(
            source="surveillance",
            signal=(
                "ELEVATED"
                if surveillance_change >= 25
                else "MODERATE"
                if surveillance_change > 0
                else "STABLE"
            ),
            summary=(
                "Recent reported cases are above the configured "
                "surveillance baseline."
                if surveillance_change > 0
                else
                "Recent reported cases are not above the configured "
                "surveillance baseline."
            ),
            observed_value=(
                f"{surveillance['recent_week_cases']} cases; "
                f"{surveillance_change}% change from baseline"
            ),
            data_status="SYNTHETIC DATA",
            interpretation_type="OBSERVED DATA",
            uncertainty=[
                "Surveillance values are synthetic demonstration data.",
            ],
        )
    )

    hospital_signal = _signal_value(
        hospital.get("signal")
    )

    evidence.append(
        EvidenceItem(
            source="hospital",
            signal=hospital_signal,
            summary=(
                "Hospital syndrome reporting contains an "
                f"{hospital_signal.lower()} signal."
            ),
            observed_value=(
                f"{hospital['gastrointestinal_syndrome_count']} "
                "gastrointestinal syndrome cases; "
                f"{hospital['hospitalization_count']} "
                "hospitalizations"
            ),
            data_status="SYNTHETIC DATA",
            interpretation_type="OBSERVED DATA",
            uncertainty=[
                "Hospital values are synthetic demonstration data.",
            ],
        )
    )

    laboratory_signal = _signal_value(
        laboratory.get("signal")
    )

    evidence.append(
        EvidenceItem(
            source="laboratory",
            signal=laboratory_signal,
            summary=(
                "Laboratory reporting contains an "
                f"{laboratory_signal.lower()} signal."
            ),
            observed_value=(
                f"{laboratory['positive_samples']} positive samples "
                f"out of {laboratory['samples_tested']} tested; "
                f"{laboratory['positivity_rate_percent']}% positivity"
            ),
            data_status="SYNTHETIC DATA",
            interpretation_type="OBSERVED DATA",
            uncertainty=[
                "Laboratory values are synthetic demonstration data.",
                "The values are not linked to real specimens.",
            ],
        )
    )

    environmental_signal = _signal_value(
        environmental.get("signal")
    )

    evidence.append(
        EvidenceItem(
            source="environmental",
            signal=environmental_signal,
            summary=(
                "Environmental reporting contains an "
                f"{environmental_signal.lower()} signal."
            ),
            observed_value=(
                f"Rainfall trend: {environmental['rainfall_trend']}; "
                f"flooding reports: {environmental['flooding_reports']}; "
                f"water quality signal: "
                f"{environmental['water_quality_signal']}"
            ),
            data_status="SYNTHETIC DATA",
            interpretation_type="OBSERVED DATA",
            uncertainty=[
                "Environmental values are synthetic demonstration data.",
                "Environmental relationships are illustrative and do not establish causation.",
            ],
        )
    )

    geographic_evidence: list[GeographicEvidence] = []

    for signal in geographic_signals:
        cases = float(signal["cases"])
        baseline_cases = float(signal["baseline_cases"])

        geographic_evidence.append(
            GeographicEvidence(
                geography=signal["lga"],
                cases=cases,
                baseline_cases=baseline_cases,
                signal=_signal_value(
                    signal.get("signal")
                ),
                deviation_percent=_geographic_deviation(
                    cases=cases,
                    baseline_cases=baseline_cases,
                ),
            )
        )

    all_signals = [
        item.signal
        for item in evidence
    ]

    elevated_signal_count = all_signals.count(
        "ELEVATED"
    )

    moderate_signal_count = all_signals.count(
        "MODERATE"
    )

    stable_signal_count = all_signals.count(
        "STABLE"
    )

    return EvidenceAssessment(
        disease=result.disease,
        geography=result.geography,
        data_status="SYNTHETIC DATA",
        notice=(
            "SYNTHETIC DEMONSTRATION DATA - "
            "NOT FOR OFFICIAL CLINICAL ACTION"
        ),
        evidence=evidence,
        geographic_evidence=geographic_evidence,
        elevated_signal_count=elevated_signal_count,
        moderate_signal_count=moderate_signal_count,
        stable_signal_count=stable_signal_count,
        uncertainty=[
            "All evidence inputs are synthetic demonstration data.",
            "Signal classifications are based on the supplied synthetic scenario.",
            "Evidence association does not establish causation.",
        ],
        human_review_required=True,
    )