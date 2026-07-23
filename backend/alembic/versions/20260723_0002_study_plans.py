"""Create study plan tables."""

from alembic import op
import sqlalchemy as sa


revision = "20260723_0002"
down_revision = "20260721_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "study_plans",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("plan_date", sa.Date(), nullable=False),
        sa.Column("available_minutes", sa.Integer(), nullable=False),
        sa.Column("focus", sa.String(length=120), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_study_plans_user_id", "study_plans", ["user_id"])
    op.create_index("ix_study_plans_plan_date", "study_plans", ["plan_date"])
    op.create_table(
        "study_plan_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("study_plan_id", sa.Uuid(), nullable=False),
        sa.Column("problem_reference_id", sa.Uuid(), nullable=True),
        sa.Column("item_type", sa.String(length=20), nullable=False),
        sa.Column("estimated_minutes", sa.Integer(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["problem_reference_id"], ["problem_references.id"]),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_study_plan_items_study_plan_id", "study_plan_items", ["study_plan_id"])


def downgrade() -> None:
    op.drop_index("ix_study_plan_items_study_plan_id", table_name="study_plan_items")
    op.drop_table("study_plan_items")
    op.drop_index("ix_study_plans_plan_date", table_name="study_plans")
    op.drop_index("ix_study_plans_user_id", table_name="study_plans")
    op.drop_table("study_plans")
