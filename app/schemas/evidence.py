from typing import Literal

from pydantic import BaseModel, ConfigDict


EvidenceSignal = Literal[
    "STABLE",
    "MODERATE",
    "ELEVATED",
    "UNKNOWN",
]


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    signal: EvidenceSignal
    summary: str
    observed_value: str | None = None
    data_status: str
    interpretation_type: str
    uncertainty: list[str]


class GeographicEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    geography: str
    cases: float
    baseline_cases: float
    signal: EvidenceSignal
    deviation_percent: float


class EvidenceAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    disease: str
    geography: str

    data_status: str
    notice: str

    evidence: list[EvidenceItem]
    geographic_evidence: list[GeographicEvidence]

    elevated_signal_count: int
    moderate_signal_count: int
    stable_signal_count: int

    uncertainty: list[str]

    human_review_required: bool