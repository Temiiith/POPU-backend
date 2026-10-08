from typing import Literal

from pydantic import BaseModel, ConfigDict


RiskLevel = Literal[
    "LOW",
    "MODERATE",
    "ELEVATED",
]


class RiskAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    disease: str
    geography: str

    risk_level: RiskLevel
    risk_score: float

    evidence_signal_count: int
    elevated_signal_count: int
    moderate_signal_count: int
    stable_signal_count: int

    contributing_factors: list[str]

    data_status: str
    notice: str

    uncertainty: list[str]

    human_review_required: bool