
from multiprocessing import get_context
from queue import Empty

from app.core.config import settings
from app.services.llm.gemini_provider import GeminiProvider
from app.services.llm.natlas_provider import NatlasProvider
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.provider import LLMResult


PROVIDER_TIMEOUT_SECONDS = 30


def _run_provider(provider_name: str, prompt: str, result_queue) -> None:
    try:
        if provider_name == "gemini":
            provider = GeminiProvider()
        elif provider_name == "openai":
            provider = OpenAIProvider()
        elif provider_name == "natlas":
            provider = NatlasProvider()
        else:
            raise RuntimeError(
                f"Unsupported LLM provider: {provider_name}"
            )

        result = provider.generate(prompt)

        result_queue.put(
            {
                "success": True,
                "provider": result.provider,
                "model": result.model,
                "text": result.text,
            }
        )

    except Exception as exc:
        result_queue.put(
            {
                "success": False,
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
        )


class LLMOrchestrator:
    def __init__(self) -> None:
        self.providers: list[str] = []

        if settings.llm_primary_provider == "gemini":
            if settings.gemini_api_key:
                self.providers.append("gemini")

            if settings.openai_api_key:
                self.providers.append("openai")

        elif settings.llm_primary_provider == "openai":
            if settings.openai_api_key:
                self.providers.append("openai")

            if settings.gemini_api_key:
                self.providers.append("gemini")

        if settings.natlas_endpoint_url:
            self.providers.append("natlas")

    def generate(self, prompt: str) -> LLMResult:
        if not self.providers:
            raise RuntimeError("No LLM provider is configured.")

        last_error: Exception | None = None

        for provider_name in self.providers:
            ctx = get_context("spawn")
            result_queue = ctx.Queue()

            process = ctx.Process(
                target=_run_provider,
                args=(provider_name, prompt, result_queue),
            )

            process.start()
            process.join(timeout=PROVIDER_TIMEOUT_SECONDS)

            if process.is_alive():
                print(
                    f"LLM provider '{provider_name}' timed out after "
                    f"{PROVIDER_TIMEOUT_SECONDS} seconds."
                )

                process.terminate()
                process.join(timeout=2)
                result_queue.close()
                result_queue.cancel_join_thread()

                last_error = TimeoutError(
                    f"{provider_name} timed out after "
                    f"{PROVIDER_TIMEOUT_SECONDS} seconds."
                )
                continue

            try:
                result = result_queue.get(timeout=1)
            except Empty:
                result_queue.close()

                last_error = RuntimeError(
                    f"LLM provider '{provider_name}' exited "
                    "without a result."
                )
                continue
            finally:
                if not process.is_alive():
                    process.join(timeout=1)

            result_queue.close()

            if not result["success"]:
                print(
                    f"LLM provider '{provider_name}' failed: "
                    f"{result['error_type']}: {result['error']}"
                )

                last_error = RuntimeError(result["error"])
                continue

            return LLMResult(
                provider=result["provider"],
                model=result["model"],
                text=result["text"],
                fallback_used=provider_name != self.providers[0],
            )

        raise RuntimeError(
            f"All configured LLM providers failed: {last_error}"
        )