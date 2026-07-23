import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401
from app.db.base import Base
from app.db.session import get_session
from app.main import create_app


class LearningRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.app = create_app()

        def override_get_session():
            session = self.session_factory()
            try:
                yield session
            finally:
                session.close()

        self.app.dependency_overrides[get_session] = override_get_session
        self.client = TestClient(self.app)

    def tearDown(self) -> None:
        self.app.dependency_overrides.clear()
        self.engine.dispose()

    def test_attempt_creation_returns_a_future_review_date(self) -> None:
        create_response = self.client.post(
            "/api/v1/attempts",
            json={
                "problem": {
                    "platform": "leetcode",
                    "url": "https://leetcode.com/problems/two-sum/",
                    "title": "Two Sum",
                },
                "outcome": "solved_independently",
                "duration_minutes": 18,
                "language": "python",
            },
        )

        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(create_response.json()["interval_days"], 1)
        self.assertIn("next_review_at", create_response.json())

    def test_plan_creates_new_problem_time_slots_without_a_problem_bank(self) -> None:
        response = self.client.post(
            "/api/v1/plans",
            json={"available_minutes": 60},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["allocated_minutes"], 60)
        self.assertEqual(
            [item["item_type"] for item in response.json()["items"]],
            ["new", "new"],
        )
