from typing import Literal

from pydantic import BaseModel, ConfigDict


IntegratedRiskLevel = Literal[
    "LOW",
    "MODERATE",
    "ELEVATED",
]


class RiskComponent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    signal: str
    contribution: float
    explanation: str


class IntegratedRiskAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    disease: str
    geography: str

    risk_level: IntegratedRiskLevel
    risk_score: float

    components: list[RiskComponent]

    key_factors: list[str]

    data_status: str
    notice: str

    uncertainty: list[str]

    human_review_required: bool