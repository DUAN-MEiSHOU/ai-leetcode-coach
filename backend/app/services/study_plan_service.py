from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.repositories.learning_repository import LearningRepository
from app.schemas.learning import (
    StudyPlanCreateRequest,
    StudyPlanItemResponse,
    StudyPlanResponse,
)

REVIEW_MINUTES = 15
NEW_PROBLEM_MINUTES = 30


class StudyPlanService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repository = LearningRepository(session)

    def create_plan(self, request: StudyPlanCreateRequest) -> StudyPlanResponse:
        user = self._repository.get_or_create_local_user()
        due_reviews = self._repository.list_due_reviews(
            user_id=user.id,
            now=datetime.now(timezone.utc),
            limit=max(1, request.available_minutes // REVIEW_MINUTES),
        )
        plan = self._repository.create_study_plan(
            user_id=user.id,
            plan_date=date.today(),
            available_minutes=request.available_minutes,
            focus=request.focus,
        )

        remaining_minutes = request.available_minutes
        items: list[StudyPlanItemResponse] = []
        position = 1
        for schedule in due_reviews:
            if remaining_minutes < REVIEW_MINUTES:
                break
            problem = self._repository.get_problem(schedule.problem_reference_id)
            if problem is None:
                continue
            self._repository.add_study_plan_item(
                study_plan_id=plan.id,
                problem_reference_id=problem.id,
                item_type="review",
                estimated_minutes=REVIEW_MINUTES,
                reason="This problem is due for review.",
                position=position,
            )
            items.append(
                StudyPlanItemResponse(
                    item_type="review",
                    estimated_minutes=REVIEW_MINUTES,
                    reason="This problem is due for review.",
                    position=position,
                    problem_reference_id=problem.id,
                    title=problem.title,
                    url=problem.url,
                )
            )
            remaining_minutes -= REVIEW_MINUTES
            position += 1

        while remaining_minutes >= NEW_PROBLEM_MINUTES:
            self._repository.add_study_plan_item(
                study_plan_id=plan.id,
                problem_reference_id=None,
                item_type="new",
                estimated_minutes=NEW_PROBLEM_MINUTES,
                reason="Choose one new problem in LeetCode; no problem bank is stored here.",
                position=position,
            )
            items.append(
                StudyPlanItemResponse(
                    item_type="new",
                    estimated_minutes=NEW_PROBLEM_MINUTES,
                    reason="Choose one new problem in LeetCode; no problem bank is stored here.",
                    position=position,
                )
            )
            remaining_minutes -= NEW_PROBLEM_MINUTES
            position += 1

        self._session.commit()
        return StudyPlanResponse(
            id=plan.id,
            plan_date=datetime.combine(plan.plan_date, datetime.min.time(), tzinfo=timezone.utc),
            available_minutes=request.available_minutes,
            allocated_minutes=request.available_minutes - remaining_minutes,
            remaining_minutes=remaining_minutes,
            items=items,
        )
