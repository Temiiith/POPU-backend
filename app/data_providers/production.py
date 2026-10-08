from app.data_providers.base import EpidemiologyDataProvider, ScenarioLookupResult


class ProductionDataProvider(EpidemiologyDataProvider):
    id = "production-provider-pending"
    name = "POPU Production Data Provider"
    mode = "production"

    def get_scenario(self, disease: str, geography: str) -> ScenarioLookupResult:
        return ScenarioLookupResult(
            status="SOURCE_NOT_CONFIGURED",
            provider=self.name,
            mode=self.mode,
            disease=disease,
            geography=geography,
            scenario=None,
            message="No production epidemiological source is connected.",
        )
