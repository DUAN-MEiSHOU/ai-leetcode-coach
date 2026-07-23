from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


AttemptOutcome = Literal[
    "solved_independently",
    "solved_with_hints",
    "viewed_solution",
    "gave_up",
    "reviewed_easily",
    "struggled",
]


class ProblemReferenceInput(BaseModel):
    platform: str = Field(default="leetcode", min_length=1, max_length=40)
    url: str = Field(min_length=1, max_length=500)
    title: str | None = Field(default=None, max_length=300)
    slug: str | None = Field(default=None, max_length=300)
    difficulty: str | None = Field(default=None, max_length=30)


class AttemptCreateRequest(BaseModel):
    problem: ProblemReferenceInput
    outcome: AttemptOutcome
    duration_minutes: int | None = Field(default=None, ge=0, le=1_440)
    max_hint_level_used: int = Field(default=0, ge=0, le=6)
    used_hint: bool = False
    viewed_full_solution: bool = False
    language: str | None = Field(default=None, max_length=40)
    notes: str | None = Field(default=None, max_length=2_000)


class AttemptCreateResponse(BaseModel):
    id: UUID
    problem_reference_id: UUID
    outcome: AttemptOutcome
    attempted_at: datetime
    review_schedule_id: UUID
    next_review_at: datetime
    interval_days: int


class DueReviewResponse(BaseModel):
    schedule_id: UUID
    problem_reference_id: UUID
    platform: str
    url: str
    title: str | None
    next_review_at: datetime
    interval_days: int
    review_streak: int
    last_outcome: AttemptOutcome | None


class StudyPlanCreateRequest(BaseModel):
    available_minutes: int = Field(ge=15, le=480)
    focus: str | None = Field(default=None, max_length=120)


class StudyPlanItemResponse(BaseModel):
    item_type: Literal["review", "new"]
    estimated_minutes: int
    reason: str
    position: int
    problem_reference_id: UUID | None = None
    title: str | None = None
    url: str | None = None


class StudyPlanResponse(BaseModel):
    id: UUID
    plan_date: datetime
    available_minutes: int
    allocated_minutes: int
    remaining_minutes: int
    items: list[StudyPlanItemResponse]
