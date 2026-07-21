from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ReviewSchedule(Base):
    __tablename__ = "review_schedules"
    __table_args__ = (
        UniqueConstraint("user_id", "problem_reference_id", name="uq_review_user_problem"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    problem_reference_id: Mapped[UUID] = mapped_column(
        ForeignKey("problem_references.id"), index=True
    )
    next_review_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    interval_days: Mapped[int] = mapped_column(Integer, default=0)
    review_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_outcome: Mapped[str | None] = mapped_column(String(40), nullable=True)
    last_attempt_id: Mapped[UUID | None] = mapped_column(ForeignKey("attempts.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
