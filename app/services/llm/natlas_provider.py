from app.core.config import settings
from app.services.llm.provider import LLMResult


class NatlasProvider:
    name = "natlas"

    def __init__(self) -> None:
        self.model = settings.natlas_model

        if not settings.natlas_endpoint_url:
            raise RuntimeError(
                "N-ATLaS endpoint is not configured."
            )

        self.endpoint_url = settings.natlas_endpoint_url
        self.api_key = settings.natlas_api_key

    def generate(self, prompt: str) -> LLMResult:
        raise RuntimeError(
            "N-ATLaS inference is not implemented yet. "
            "Configure a deployed N-ATLaS endpoint before enabling this provider."
        )