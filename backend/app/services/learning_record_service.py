from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.repositories.learning_repository import LearningRepository
from app.schemas.learning import AttemptCreateRequest, AttemptCreateResponse, DueReviewResponse
from app.services.review_service import ReviewService


class LearningRecordService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repository = LearningRepository(session)
        self._review_service = ReviewService()

    def record_attempt(self, request: AttemptCreateRequest) -> AttemptCreateResponse:
        user = self._repository.get_or_create_local_user()
        problem = self._repository.get_or_create_problem(**request.problem.model_dump())
        attempt = self._repository.create_attempt(
            user_id=user.id,
            problem_reference_id=problem.id,
            outcome=request.outcome,
            duration_minutes=request.duration_minutes,
            max_hint_level_used=request.max_hint_level_used,
            used_hint=request.used_hint,
            viewed_full_solution=request.viewed_full_solution,
            language=request.language,
            notes=request.notes,
        )
        schedule = self._repository.ensure_review_schedule(
            user_id=user.id,
            problem_reference_id=problem.id,
            attempt=attempt,
        )
        decision = self._review_service.calculate_next_review(
            attempt.outcome,
            schedule.review_streak,
        )
        schedule = self._repository.update_review_schedule(
            schedule=schedule,
            attempt=attempt,
            interval_days=decision.interval_days,
            review_streak=decision.review_streak,
            next_review_at=datetime.now(timezone.utc) + timedelta(days=decision.interval_days),
        )
        self._session.commit()
        self._session.refresh(attempt)
        self._session.refresh(schedule)

        return AttemptCreateResponse(
            id=attempt.id,
            problem_reference_id=problem.id,
            outcome=attempt.outcome,
            attempted_at=attempt.attempted_at,
            review_schedule_id=schedule.id,
            next_review_at=schedule.next_review_at,
            interval_days=schedule.interval_days,
        )

    def list_due_reviews(self, limit: int) -> list[DueReviewResponse]:
        user = self._repository.get_or_create_local_user()
        schedules = self._repository.list_due_reviews(
            user_id=user.id,
            now=datetime.now(timezone.utc),
            limit=limit,
        )
        self._session.commit()

        responses = []
        for schedule in schedules:
            problem = self._repository.get_problem(schedule.problem_reference_id)
            if problem is None:
                continue
            responses.append(
                DueReviewResponse(
                    schedule_id=schedule.id,
                    problem_reference_id=problem.id,
                    platform=problem.platform,
                    url=problem.url,
                    title=problem.title,
                    next_review_at=schedule.next_review_at,
                    interval_days=schedule.interval_days,
                    review_streak=schedule.review_streak,
                    last_outcome=schedule.last_outcome,
                )
            )
        return responses
