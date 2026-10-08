from dataclasses import dataclass
from typing import Protocol


@dataclass
class LLMResult:
    provider: str
    model: str
    text: str
    fallback_used: bool = False


class LLMProvider(Protocol):
    name: str
    model: str

    def generate(self, prompt: str) -> LLMResult:
        ...