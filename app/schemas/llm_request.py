from pydantic import BaseModel, ConfigDict, Field


class LLMInterpretationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request: str = Field(min_length=3)
    forecast_horizon_days: int = Field(default=14, ge=1, le=30)