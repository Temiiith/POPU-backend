from app.data_providers.registry import get_data_provider
from app.data_providers.base import ScenarioLookupResult


def get_scenario(
    disease: str,
    geography: str,
) -> ScenarioLookupResult:
    provider = get_data_provider("synthetic_demo")

    return provider.get_scenario(
        disease=disease,
        geography=geography,
    )