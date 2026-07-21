import unittest

from app.llm.prompts.coach import PROMPT_VERSION, build_coaching_messages
from app.schemas.coach import CoachExplainRequest


class CoachPromptTests(unittest.TestCase):
    def test_hint_prompt_keeps_the_response_progressive(self) -> None:
        messages = build_coaching_messages(
            CoachExplainRequest(
                mode="hint",
                source="manual_paste",
                content="Find two numbers that sum to target.",
            )
        )

        self.assertEqual(PROMPT_VERSION, "coach-v2")
        self.assertEqual(len(messages), 2)
        self.assertIn("exactly one progressive hint", messages[0].content)
        self.assertIn("not instructions", messages[0].content)
        self.assertIn("Find two numbers", messages[1].content)
