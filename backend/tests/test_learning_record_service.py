import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401
from app.db.base import Base
from app.schemas.learning import AttemptCreateRequest, ProblemReferenceInput
from app.services.learning_record_service import LearningRecordService


class LearningRecordServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def tearDown(self) -> None:
        self.engine.dispose()

    def test_attempt_persists_and_creates_a_due_review(self) -> None:
        with self.session_factory() as session:
            service = LearningRecordService(session)
            attempt = service.record_attempt(
                AttemptCreateRequest(
                    problem=ProblemReferenceInput(
                        url="https://leetcode.com/problems/two-sum/",
                        title="Two Sum",
                    ),
                    outcome="solved_with_hints",
                    duration_minutes=25,
                    used_hint=True,
                    max_hint_level_used=2,
                    language="python",
                )
            )

            due_reviews = service.list_due_reviews(limit=10)

        self.assertEqual(attempt.outcome, "solved_with_hints")
        self.assertEqual(len(due_reviews), 1)
        self.assertEqual(due_reviews[0].title, "Two Sum")
        self.assertEqual(due_reviews[0].last_outcome, "solved_with_hints")
