from app.schemas.investigation import InvestigationResult


def build_investigation_prompt(result: InvestigationResult) -> str:
    evidence_lines = []

    for item in result.evidence.evidence:
        evidence_lines.append(
            f"- {item.source}: {item.signal} — {item.summary} "
            f"({item.observed_value})"
        )

    geography_lines = []

    for item in result.evidence.geographic_evidence:
        geography_lines.append(
            f"- {item.geography}: {item.signal} — "
            f"{item.cases} cases vs {item.baseline_cases} baseline "
            f"({item.deviation_percent}% deviation)"
        )

    return f"""
You are the AI interpretation layer of POPU, an epidemiological
intelligence platform.

Your job is to explain the structured investigation findings clearly
and concisely for a human epidemiologist.

IMPORTANT:
Interpret ONLY the structured evidence supplied below.

STRICT RULES:
- Do not calculate new epidemiological values.
- Do not invent, estimate, or modify values.
- Do not claim that an outbreak is confirmed.
- Do not present a forecast risk score as an outbreak probability.
- Clearly distinguish synthetic data from model output.
- Explain important uncertainty and limitations.
- Human expert review is required.
- Do not recommend autonomous public-health action.
- Do not repeat every data point unless it is important to understanding
  the signal.

OUTPUT FORMAT:

Write exactly 3 short paragraphs.

Paragraph 1 — FINDING:
State the disease, geography, overall signal, integrated risk level and
the most important reason POPU flagged the investigation.

Paragraph 2 — EVIDENCE:
Summarize the strongest supporting signals across the available
surveillance, hospital, laboratory, environmental, geographic, or
forecast evidence. Mention only the most decision-relevant values.

Paragraph 3 — INTERPRETATION & LIMITATIONS:
Explain what the findings do NOT establish, distinguish synthetic data
from model output, mention the most important model/data limitation,
and state that human epidemiological review is required before
operational action.

STYLE:
- Maximum 180 words.
- Professional epidemiological language.
- Clear and direct.
- No Markdown headings.
- No bullet points.
- No numbered sections.
- No tables.
- No introductory phrase such as "Here is the interpretation."

INVESTIGATION
Disease: {result.disease}
Geography: {result.geography}
Overall signal: {result.overall_signal}
Data status: {result.data_status}

KEY FINDINGS
{chr(10).join(f"- {item}" for item in result.key_findings)}

ANOMALY
Status: {result.anomaly.status}
Observed: {result.anomaly.observed_value}
Baseline: {result.anomaly.baseline_value}
Deviation: {result.anomaly.percent_deviation}%
Method: {result.anomaly.method}

EVIDENCE SOURCES
{chr(10).join(evidence_lines)}

GEOGRAPHIC SIGNALS
{chr(10).join(geography_lines)}

FORECAST
Risk level: {result.forecast.risk_level}
Risk score: {result.forecast.risk_score}
Predicted values: {result.forecast.predicted_values}
Model: {result.forecast.model}

INTEGRATED RISK
Level: {result.integrated_risk.risk_level}
Risk score: {result.integrated_risk.risk_score}

UNCERTAINTY
{chr(10).join(f"- {item}" for item in result.uncertainty)}

Return only the three paragraphs.
""".strip()