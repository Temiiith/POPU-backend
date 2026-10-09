
from google import genai

from app.core.config import settings
from app.services.llm.provider import LLMResult


class GeminiProvider:
    name = "gemini"

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError("Gemini API key is not configured.")

        self.model = settings.llm_model_gemini
        self.client = genai.Client(
            api_key=settings.gemini_api_key,
            http_options={
                "timeout": 10000,
                "retry_options": {
                    "attempts": 2,
                },
            },
        )

    def generate(self, prompt: str) -> LLMResult:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        text = response.text

        if not text or not text.strip():
            raise RuntimeError(
                "Gemini returned an empty interpretation."
            )

        return LLMResult(
            provider=self.name,
            model=self.model,
            text=text.strip(),
        )