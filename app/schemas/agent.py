from typing import Literal

from pydantic import BaseModel, ConfigDict


AgentIntentType = Literal[
    "INVESTIGATE",
    "UNKNOWN",
]


class AgentIntent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: AgentIntentType
    disease: str | None = None
    geography: str | None = None
    forecast_horizon_days: int = 7
    original_request: str