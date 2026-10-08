from openai import OpenAI

from app.core.config import settings
from app.services.llm.provider import LLMResult


class OpenAIProvider:
    name = "openai"

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OpenAI API key is not configured.")

        self.model = settings.llm_model_openai
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate(self, prompt: str) -> LLMResult:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return LLMResult(
            provider=self.name,
            model=self.model,
            text=response.output_text,
        )