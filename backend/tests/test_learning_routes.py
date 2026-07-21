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

    def test_attempt_creation_is_visible_in_due_reviews(self) -> None:
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

        due_response = self.client.get("/api/v1/reviews/due")

        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(due_response.status_code, 200)
        self.assertEqual(len(due_response.json()), 1)
        self.assertEqual(due_response.json()[0]["title"], "Two Sum")
