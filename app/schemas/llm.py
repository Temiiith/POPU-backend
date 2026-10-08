from pydantic import BaseModel, ConfigDict


class LLMInterpretation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str
    fallback_used: bool

    interpretation: str

    uncertainty: list[str]

    human_review_required: bool
