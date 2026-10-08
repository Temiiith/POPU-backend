from fastapi import APIRouter, HTTPException, Query

from app.schemas.anomaly import AnomalyResult
from app.schemas.forecast import ForecastResult
from app.services.anomaly_service import detect_anomaly
from app.services.forecast_service import forecast_disease_risk
from app.schemas.evidence import EvidenceAssessment
from app.services.evidence_service import assess_evidence
from app.schemas.risk import RiskAssessment
from app.services.risk_service import assess_risk
from app.schemas.investigation import InvestigationResult
from app.services.investigation_service import investigate
from app.services.risk_fusion_service import assess_integrated_risk
from app.schemas.risk_fusion import IntegratedRiskAssessment


router = APIRouter(
    prefix="/analysis",
    tags=["epidemiological analysis"],
)


@router.get(
    "/anomaly",
    response_model=AnomalyResult,
)
def anomaly(
    disease: str = Query(..., min_length=1),
    geography: str = Query(..., min_length=1),
) -> AnomalyResult:
    result = detect_anomaly(
        disease=disease,
        geography=geography,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Anomaly analysis unavailable for the requested scenario.",
        )

    return result


@router.get(
    "/forecast",
    response_model=ForecastResult,
)
def forecast(
    disease: str = Query(..., min_length=1),
    geography: str = Query(..., min_length=1),
    horizon_days: int = Query(
        7,
        ge=1,
        le=30,
    ),
) -> ForecastResult:
    result = forecast_disease_risk(
        disease=disease,
        geography=geography,
        horizon_days=horizon_days,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Forecast unavailable for the requested scenario.",
        )

    return result
@router.get("/evidence", response_model=EvidenceAssessment)
def evidence(
    disease: str = Query(..., min_length=1),
    geography: str = Query(..., min_length=1),
) -> EvidenceAssessment:
    result = assess_evidence(
        disease=disease,
        geography=geography,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Evidence assessment unavailable for the requested scenario.",
        )

    return result
@router.get("/risk", response_model=RiskAssessment)
def risk(
    disease: str = Query(..., min_length=1),
    geography: str = Query(..., min_length=1),
) -> RiskAssessment:
    result = assess_risk(
        disease=disease,
        geography=geography,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Risk assessment unavailable for the requested scenario.",
        )

    return result

@router.get(
    "/investigation",
    response_model=InvestigationResult,
)
def investigation(
    disease: str = Query(..., min_length=1),
    geography: str = Query(..., min_length=1),
    forecast_horizon_days: int = Query(
        7,
        ge=1,
        le=30,
    ),
) -> InvestigationResult:
    result = investigate(
        disease=disease,
        geography=geography,
        forecast_horizon_days=forecast_horizon_days,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Investigation unavailable for the "
                "requested scenario."
            ),
        )

    return result

@router.get(
    "/risk/integrated",
    response_model=IntegratedRiskAssessment,
)
def get_integrated_risk(
    disease: str = Query(..., min_length=1),
    geography: str = Query(..., min_length=1),
    forecast_horizon_days: int = Query(
        7,
        ge=1,
        le=30,
    ),
):
    result = assess_integrated_risk(
        disease=disease,
        geography=geography,
        forecast_horizon_days=forecast_horizon_days,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No synthetic scenario found for the requested disease and geography.",
        )

    return result