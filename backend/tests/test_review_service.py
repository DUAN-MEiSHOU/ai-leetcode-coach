import unittest

from app.services.review_service import ReviewService


class ReviewServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ReviewService()

    def test_independent_success_advances_interval(self) -> None:
        decision = self.service.calculate_next_review("solved_independently", current_streak=2)

        self.assertEqual(decision.review_streak, 3)
        self.assertEqual(decision.interval_days, 7)

    def test_hints_keep_the_current_level(self) -> None:
        decision = self.service.calculate_next_review("solved_with_hints", current_streak=3)

        self.assertEqual(decision.review_streak, 3)
        self.assertEqual(decision.interval_days, 7)

    def test_struggle_resets_to_one_day(self) -> None:
        decision = self.service.calculate_next_review("struggled", current_streak=5)

        self.assertEqual(decision.review_streak, 0)
        self.assertEqual(decision.interval_days, 1)
