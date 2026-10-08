from pydantic import BaseModel, ConfigDict

from app.schemas.anomaly import AnomalyResult
from app.schemas.evidence import EvidenceAssessment
from app.schemas.forecast import ForecastResult
from app.schemas.risk import RiskAssessment
from app.schemas.risk_fusion import IntegratedRiskAssessment


class InvestigationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    disease: str
    geography: str

    anomaly: AnomalyResult
    evidence: EvidenceAssessment
    forecast: ForecastResult

    # Legacy risk assessment retained for compatibility.
    risk: RiskAssessment

    # Primary integrated POPU risk assessment.
    integrated_risk: IntegratedRiskAssessment

    overall_signal: str

    key_findings: list[str]

    data_status: str
    notice: str

    uncertainty: list[str]

    human_review_required: bool