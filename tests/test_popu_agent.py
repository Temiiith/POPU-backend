from pydantic import BaseModel, ConfigDict, Field


class AgentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request: str = Field(..., min_length=1)
    forecast_horizon_days: int = Field(
        default=7,
        ge=1,
        le=30,
    )