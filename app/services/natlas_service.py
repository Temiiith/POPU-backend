from app.core.config import settings


class NatlasService:
    def __init__(self) -> None:
        self.endpoint_url = settings.natlas_endpoint_url
        self.api_key = settings.natlas_api_key
        self.model = settings.natlas_model

    def is_configured(self) -> bool:
        return bool(self.endpoint_url)

    def status(self) -> dict[str, object]:
        return {
            "configured": self.is_configured(),
            "model": self.model,
            "endpoint_configured": bool(self.endpoint_url),
        }