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
        self.assertEqual(response.prompt_version, "coach-v2")
        self.assertIn("returns the value", response.explanation)
        self.assertIsNotNone(provider.last_request)
        self.assertEqual(len(provider.last_request.messages), 2)
        self.assertIn("explain the selected line", provider.last_request.messages[0].content.lower())

    async def test_python_request_adds_deterministic_context(self) -> None:
        provider = FakeProvider()
        service = CoachExplanationService(provider)

        response = await service.explain(
            CoachExplainRequest(
                mode="explain_line",
                source="manual_paste",
                language="python",
                selected_line_number=2,
                content="from collections import Counter\ncounts = Counter(items)\n",
            )
        )

        self.assertIsNotNone(response.code_context)
        self.assertEqual(response.code_context.selected_line, "counts = Counter(items)")
        self.assertIn("collections.Counter", provider.last_request.messages[1].content)


if __name__ == "__main__":
    unittest.main()
