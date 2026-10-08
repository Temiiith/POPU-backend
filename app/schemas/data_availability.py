from typing import Literal

from pydantic import BaseModel, ConfigDict


DataAvailabilityStatus = Literal[
    "DATA_UNAVAILABLE",
    "SOURCE_NOT_CONFIGURED",
    "INVALID_GEOGRAPHY",
]


class DataAvailabilityResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: DataAvailabilityStatus
    disease: str
    geography: str
    provider: str
    message: str
    notice: str