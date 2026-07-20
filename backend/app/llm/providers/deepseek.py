import asyncio
from collections.abc import Mapping
from typing import Any

import httpx

from app.core.config import Settings
from app.llm.errors import LLMConfigurationError, LLMProviderError
from app.llm.types import LLMRequest, LLMResponse


class DeepSeekProvider:
    provider_name = "deepseek"

    def __init__(
        self,
        settings: Settings,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._settings = settings
        self._client = client

    async def generate(self, request: LLMRequest) -> LLMResponse:
        if not self._settings.deepseek_api_key:
            raise LLMConfigurationError("DEEPSEEK_API_KEY is not configured.")

        payload = {
            "model": self._settings.deepseek_model,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in request.messages
            ],
            "temperature": request.temperature,
        }

        last_error: Exception | None = None
        for attempt in range(self._settings.llm_max_retries + 1):
            try:
                data = await self._post_chat_completion(payload)
                content = self._extract_content(data)
                return LLMResponse(
                    content=content,
                    model=self._settings.deepseek_model,
                    provider=self.provider_name,
                )
            except (httpx.HTTPError, LLMProviderError) as error:
                last_error = error
                if attempt >= self._settings.llm_max_retries:
                    break
                await asyncio.sleep(0.2 * (attempt + 1))

        raise LLMProviderError(f"DeepSeek request failed: {last_error}") from last_error

    async def _post_chat_completion(self, payload: dict[str, Any]) -> Mapping[str, Any]:
        headers = {
            "Authorization": f"Bearer {self._settings.deepseek_api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self._settings.deepseek_base_url.rstrip('/')}/chat/completions"

        if self._client is not None:
            response = await self._client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

        timeout = httpx.Timeout(self._settings.llm_timeout_seconds)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    def _extract_content(self, data: Mapping[str, Any]) -> str:
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise LLMProviderError("DeepSeek response is missing message content.") from error

        if not isinstance(content, str) or not content.strip():
            raise LLMProviderError("DeepSeek response content is empty.")

        return content.strip()
