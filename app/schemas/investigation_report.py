from pydantic import BaseModel, ConfigDict


class InvestigationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    disease: str
    geography: str

    summary: str

    key_findings: list[str]

    investigation_priorities: list[str]

    supporting_evidence: list[str]

    uncertainty: list[str]

    data_status: str
    notice: str

    human_review_required: bool