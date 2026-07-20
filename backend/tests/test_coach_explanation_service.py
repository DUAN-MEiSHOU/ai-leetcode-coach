import unittest

from app.llm.types import LLMRequest, LLMResponse
from app.schemas.coach import CoachExplainRequest
from app.services.coach_explanation_service import CoachExplanationService


class FakeProvider:
    def __init__(self) -> None:
        self.last_request: LLMRequest | None = None

    async def generate(self, request: LLMRequest) -> LLMResponse:
        self.last_request = request
        return LLMResponse(
            content="This line returns the value at index i.",
            model="fake-model",
            provider="fake",
        )


class CoachExplanationServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_explain_uses_provider_and_returns_response(self) -> None:
        provider = FakeProvider()
        service = CoachExplanationService(provider)

        response = await service.explain(
            CoachExplainRequest(
                mode="explain_line",
                source="manual_paste",
                language="python",
                content="return nums[i]",
            )
        )

        self.assertEqual(response.status, "ok")
        self.assertEqual(response.provider, "fake")
        self.assertEqual(response.model, "fake-model")
        self.assertIn("returns the value", response.explanation)
        self.assertIsNotNone(provider.last_request)
        self.assertEqual(len(provider.last_request.messages), 2)


if __name__ == "__main__":
    unittest.main()
