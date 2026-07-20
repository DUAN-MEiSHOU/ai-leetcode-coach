from typing import Protocol

from app.llm.types import LLMRequest, LLMResponse


class LLMProvider(Protocol):
    async def generate(self, request: LLMRequest) -> LLMResponse:
        ...
