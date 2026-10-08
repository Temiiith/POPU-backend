from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    data_mode: str
    production_data_connected: bool
    synthetic_notice: str
