import unittest

import httpx

from app.core.config import Settings
from app.llm.errors import LLMConfigurationError, LLMProviderError
from app.llm.providers.deepseek import DeepSeekProvider
from app.llm.types import LLMMessage, LLMRequest


def _request() -> LLMRequest:
    return LLMRequest(messages=[LLMMessage(role="user", content="Explain this.")])


class DeepSeekProviderTests(unittest.IsolatedAsyncioTestCase):
    async def test_generate_requires_api_key(self) -> None:
        provider = DeepSeekProvider(Settings(deepseek_api_key=""))

        with self.assertRaises(LLMConfigurationError):
            await provider.generate(_request())

    async def test_generate_extracts_content_from_mock_response(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.headers["authorization"], "Bearer test-key")
            return httpx.Response(
                200,
                json={
                    "choices": [
                        {"message": {"content": "Use a hash map to track complements."}}
                    ]
                },
            )

        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        provider = DeepSeekProvider(Settings(deepseek_api_key="test-key"), client=client)

        try:
            response = await provider.generate(_request())
        finally:
            await client.aclose()

        self.assertEqual(response.provider, "deepseek")
        self.assertEqual(response.model, "deepseek-chat")
        self.assertIn("hash map", response.content)

    async def test_generate_rejects_empty_content(self) -> None:
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(
                    200,
                    json={"choices": [{"message": {"content": ""}}]},
                )
            )
        )
        provider = DeepSeekProvider(
            Settings(deepseek_api_key="test-key", llm_max_retries=0),
            client=client,
        )

        try:
            with self.assertRaises(LLMProviderError):
                await provider.generate(_request())
        finally:
            await client.aclose()


if __name__ == "__main__":
    unittest.main()
