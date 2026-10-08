from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal


DataMode = Literal["synthetic_demo", "production"]
DataAvailabilityStatus = Literal[
    "AVAILABLE",
    "DATA_UNAVAILABLE",
    "SOURCE_NOT_CONFIGURED",
    "INVALID_GEOGRAPHY",
]


@dataclass(frozen=True)
class ScenarioLookupResult:
    status: DataAvailabilityStatus
    provider: str
    mode: DataMode
    disease: str
    geography: str
    scenario: dict | None
    message: str


class EpidemiologyDataProvider(ABC):
    id: str
    name: str
    mode: DataMode

    @abstractmethod
    def get_scenario(self, disease: str, geography: str) -> ScenarioLookupResult:
        raise NotImplementedError
