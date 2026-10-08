from app.data.synthetic_scenarios import SYNTHETIC_SCENARIOS
from app.data_providers.base import (
    EpidemiologyDataProvider,
    ScenarioLookupResult,
)


class SyntheticDataProvider(EpidemiologyDataProvider):
    id = "synthetic-demo-provider"
    name = "POPU Synthetic Scenario Provider"
    mode = "synthetic_demo"

    def get_scenario(
        self,
        disease: str,
        geography: str,
    ) -> ScenarioLookupResult:
        normalized_disease = disease.strip().lower()
        normalized_geography = geography.strip()

        disease_data = SYNTHETIC_SCENARIOS.get(normalized_disease)

        if disease_data is None:
            return ScenarioLookupResult(
                status="DATA_UNAVAILABLE",
                provider=self.name,
                mode=self.mode,
                disease=disease,
                geography=geography,
                scenario=None,
                message=(
                    f"No synthetic scenario is configured for disease "
                    f"'{disease}'."
                ),
            )

        scenario = disease_data.get(normalized_geography)

        if scenario is None:
            return ScenarioLookupResult(
                status="SOURCE_NOT_CONFIGURED",
                provider=self.name,
                mode=self.mode,
                disease=normalized_disease,
                geography=normalized_geography,
                scenario=None,
                message=(
                    f"No synthetic scenario is configured for "
                    f"'{normalized_disease}' in '{normalized_geography}'."
                ),
            )

        return ScenarioLookupResult(
            status="AVAILABLE",
            provider=self.name,
            mode=self.mode,
            disease=normalized_disease,
            geography=normalized_geography,
            scenario=scenario,
            message="Synthetic scenario retrieved successfully.",
        )