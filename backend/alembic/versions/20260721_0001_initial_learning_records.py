"""Create initial learning record tables."""

from alembic import op
import sqlalchemy as sa


revision = "20260721_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "problem_references",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("platform", sa.String(length=40), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("title", sa.String(length=300), nullable=True),
        sa.Column("slug", sa.String(length=300), nullable=True),
        sa.Column("difficulty", sa.String(length=30), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("platform", "url", name="uq_problem_platform_url"),
    )
    op.create_table(
        "attempts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("problem_reference_id", sa.Uuid(), nullable=False),
        sa.Column("attempted_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("outcome", sa.String(length=40), nullable=False),
        sa.Column("max_hint_level_used", sa.Integer(), nullable=False),
        sa.Column("used_hint", sa.Boolean(), nullable=False),
        sa.Column("viewed_full_solution", sa.Boolean(), nullable=False),
        sa.Column("language", sa.String(length=40), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["problem_reference_id"], ["problem_references.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_attempts_user_id", "attempts", ["user_id"])
    op.create_index("ix_attempts_problem_reference_id", "attempts", ["problem_reference_id"])
    op.create_table(
        "review_schedules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("problem_reference_id", sa.Uuid(), nullable=False),
        sa.Column("next_review_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("interval_days", sa.Integer(), nullable=False),
        sa.Column("review_streak", sa.Integer(), nullable=False),
        sa.Column("last_outcome", sa.String(length=40), nullable=True),
        sa.Column("last_attempt_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["last_attempt_id"], ["attempts.id"]),
        sa.ForeignKeyConstraint(["problem_reference_id"], ["problem_references.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "problem_reference_id", name="uq_review_user_problem"),
    )
    op.create_index("ix_review_schedules_user_id", "review_schedules", ["user_id"])
    op.create_index("ix_review_schedules_problem_reference_id", "review_schedules", ["problem_reference_id"])
    op.create_index("ix_review_schedules_next_review_at", "review_schedules", ["next_review_at"])


def downgrade() -> None:
    op.drop_index("ix_review_schedules_next_review_at", table_name="review_schedules")
    op.drop_index("ix_review_schedules_problem_reference_id", table_name="review_schedules")
    op.drop_index("ix_review_schedules_user_id", table_name="review_schedules")
    op.drop_table("review_schedules")
    op.drop_index("ix_attempts_problem_reference_id", table_name="attempts")
    op.drop_index("ix_attempts_user_id", table_name="attempts")
    op.drop_table("attempts")
    op.drop_table("problem_references")
    op.drop_table("users")
