from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


SignalStatus = Literal["ANOMALY", "ELEVATED"]


class SignalResult(BaseModel):
    signal_id: str
    disease: str
    geography: str

    status: SignalStatus
    severity: Literal["HIGH", "MODERATE"]

    detected_at: datetime

    baseline_value: float
    observed_value: float
    percent_deviation: float

    detection_method: str
    source: str

    summary: str

    supporting_sources: list[str] = Field(default_factory=list)
    elevated_source_count: int = 0
    moderate_source_count: int = 0
    geographic_signal_count: int = 0

    risk_level: Literal["LOW", "MODERATE", "ELEVATED"]
    risk_score: float

    forecast_risk_level: Literal["LOW", "MODERATE", "ELEVATED"]
    forecast_risk_score: float
    forecast_horizon_days: int
    forecast_direction: Literal["INCREASING", "STABLE", "DECREASING"]

    data_status: str
    notice: str

    human_review_required: bool = True
    uncertainty: list[str] = Field(default_factory=list)