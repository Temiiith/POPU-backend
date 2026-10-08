from app.core.config import settings
from app.data_providers.base import EpidemiologyDataProvider
from app.data_providers.production import ProductionDataProvider
from app.data_providers.synthetic import SyntheticDataProvider

_synthetic = SyntheticDataProvider()
_production = ProductionDataProvider()


def get_data_provider(mode: str | None = None) -> EpidemiologyDataProvider:
    selected = mode or settings.data_mode
    if selected == "production":
        return _production
    return _synthetic


def get_registry_summary() -> dict:
    provider = get_data_provider()
    return {
        "mode": provider.mode,
        "provider_id": provider.id,
        "provider_name": provider.name,
        "production_data_connected": False,
        "notice": "POPU currently runs without a connected production epidemiological feed.",
    }
