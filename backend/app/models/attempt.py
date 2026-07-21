from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    problem_reference_id: Mapped[UUID] = mapped_column(
        ForeignKey("problem_references.id"), index=True
    )
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    outcome: Mapped[str] = mapped_column(String(40))
    max_hint_level_used: Mapped[int] = mapped_column(Integer, default=0)
    used_hint: Mapped[bool] = mapped_column(Boolean, default=False)
    viewed_full_solution: Mapped[bool] = mapped_column(Boolean, default=False)
    language: Mapped[str | None] = mapped_column(String(40), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
