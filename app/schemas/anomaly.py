from typing import Literal

from pydantic import BaseModel, ConfigDict


AnomalyStatus = Literal[
    "NORMAL",
    "ELEVATED",
    "ANOMALY",
]


class AnomalyResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: AnomalyStatus

    disease: str
    geography: str

    data_status: str
    notice: str

    baseline_value: float
    observed_value: float

    absolute_deviation: float
    percent_deviation: float

    threshold_percent: float

    method: str
    model_output: str

    uncertainty: list[str]

    human_review_required: bool