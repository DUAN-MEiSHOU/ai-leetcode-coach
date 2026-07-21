from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.problem_reference import ProblemReference
from app.models.review_schedule import ReviewSchedule
from app.models.user import User

LOCAL_USER_NAME = "Local learner"


class LearningRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_or_create_local_user(self) -> User:
        user = self._session.scalar(select(User).where(User.display_name == LOCAL_USER_NAME))
        if user:
            return user

        user = User(display_name=LOCAL_USER_NAME)
        self._session.add(user)
        self._session.flush()
        return user

    def get_or_create_problem(
        self,
        *,
        platform: str,
        url: str,
        title: str | None,
        slug: str | None,
        difficulty: str | None,
    ) -> ProblemReference:
        problem = self._session.scalar(
            select(ProblemReference).where(
                ProblemReference.platform == platform,
                ProblemReference.url == url,
            )
        )
        if problem:
            problem.title = title or problem.title
            problem.slug = slug or problem.slug
            problem.difficulty = difficulty or problem.difficulty
            return problem

        problem = ProblemReference(
            platform=platform,
            url=url,
            title=title,
            slug=slug,
            difficulty=difficulty,
        )
        self._session.add(problem)
        self._session.flush()
        return problem

    def create_attempt(
        self,
        *,
        user_id: UUID,
        problem_reference_id: UUID,
        outcome: str,
        duration_minutes: int | None,
        max_hint_level_used: int,
        used_hint: bool,
        viewed_full_solution: bool,
        language: str | None,
        notes: str | None,
    ) -> Attempt:
        attempt = Attempt(
            user_id=user_id,
            problem_reference_id=problem_reference_id,
            outcome=outcome,
            duration_minutes=duration_minutes,
            max_hint_level_used=max_hint_level_used,
            used_hint=used_hint,
            viewed_full_solution=viewed_full_solution,
            language=language,
            notes=notes,
        )
        self._session.add(attempt)
        self._session.flush()
        return attempt

    def ensure_review_schedule(
        self,
        *,
        user_id: UUID,
        problem_reference_id: UUID,
        attempt: Attempt,
    ) -> ReviewSchedule:
        schedule = self._session.scalar(
            select(ReviewSchedule).where(
                ReviewSchedule.user_id == user_id,
                ReviewSchedule.problem_reference_id == problem_reference_id,
            )
        )
        if schedule:
            schedule.last_attempt_id = attempt.id
            schedule.last_outcome = attempt.outcome
            return schedule

        # Phase 8 owns interval selection. Until then a new record is due immediately.
        schedule = ReviewSchedule(
            user_id=user_id,
            problem_reference_id=problem_reference_id,
            next_review_at=datetime.now(timezone.utc),
            last_attempt_id=attempt.id,
            last_outcome=attempt.outcome,
        )
        self._session.add(schedule)
        self._session.flush()
        return schedule

    def list_due_reviews(self, *, user_id: UUID, now: datetime, limit: int) -> list[ReviewSchedule]:
        return list(
            self._session.scalars(
                select(ReviewSchedule)
                .where(
                    ReviewSchedule.user_id == user_id,
                    ReviewSchedule.next_review_at <= now,
                )
                .order_by(ReviewSchedule.next_review_at)
                .limit(limit)
            )
        )

    def get_problem(self, problem_id: UUID) -> ProblemReference | None:
        return self._session.get(ProblemReference, problem_id)
