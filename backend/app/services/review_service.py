from dataclasses import dataclass


REVIEW_INTERVALS_DAYS = (1, 3, 7, 16, 35, 90)


@dataclass(frozen=True)
class ReviewDecision:
    interval_days: int
    review_streak: int


class ReviewService:
    def calculate_next_review(self, outcome: str, current_streak: int) -> ReviewDecision:
        if outcome in {"solved_independently", "reviewed_easily"}:
            streak = min(current_streak + 1, len(REVIEW_INTERVALS_DAYS))
            return ReviewDecision(REVIEW_INTERVALS_DAYS[streak - 1], streak)

        if outcome == "solved_with_hints":
            streak = max(current_streak, 1)
            return ReviewDecision(REVIEW_INTERVALS_DAYS[streak - 1], streak)

        return ReviewDecision(interval_days=1, review_streak=0)
