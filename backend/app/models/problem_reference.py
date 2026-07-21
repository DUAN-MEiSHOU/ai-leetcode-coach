from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProblemReference(Base):
    __tablename__ = "problem_references"
    __table_args__ = (UniqueConstraint("platform", "url", name="uq_problem_platform_url"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    platform: Mapped[str] = mapped_column(String(40), default="leetcode")
    url: Mapped[str] = mapped_column(String(500))
    title: Mapped[str | None] = mapped_column(String(300), nullable=True)
    slug: Mapped[str | None] = mapped_column(String(300), nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
