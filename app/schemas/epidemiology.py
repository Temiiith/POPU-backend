from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ScenarioResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str
    provider: str
    mode: str
    disease: str
    geography: str
    data_status: str
    notice: str
    scenario: dict[str, Any] | None = None
    message: str


class ScenarioData(BaseModel):
    model_config = ConfigDict(extra="allow")

    disease: str
    geography: str
    data_status: str
    notice: str
    scenario_type: str
    surveillance: dict[str, Any]
    hospital: dict[str, Any]
    laboratory: dict[str, Any]
    environmental: dict[str, Any]
    geographic_signals: list[dict[str, Any]]
    uncertainty: list[str]


class ScenarioListResponse(BaseModel):
    diseases: list[str]
    geographies: list[str]
    data_status: str = Field(default="SYNTHETIC DATA")
    notice: str