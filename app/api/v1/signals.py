from fastapi import APIRouter

from app.schemas.signal import SignalResult
from app.services.signal_service import scan_all_signals


router = APIRouter(
    prefix="/signals",
    tags=["signals"],
)


@router.get(
    "/scan",
    response_model=list[SignalResult],
)
def scan_signals() -> list[SignalResult]:
    return scan_all_signals()