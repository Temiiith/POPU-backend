from typing import Literal

from pydantic import BaseModel, ConfigDict


ForecastRiskLevel = Literal[
    "LOW",
    "MODERATE",
    "ELEVATED",
]


class ForecastResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    disease: str
    geography: str

    forecast_horizon_days: int

    predicted_values: list[float]

    risk_level: ForecastRiskLevel
    risk_score: float

    confidence_interval: list[dict[str, float]]

    model: str
    model_version: str

    data_status: str
    notice: str

    uncertainty: list[str]

    human_review_required: bool