import unittest

from fastapi.testclient import TestClient

from app.main import create_app


class HealthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())

    def test_health_returns_ok(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "ok", "service": "ai-leetcode-coach-api"},
        )


if __name__ == "__main__":
    unittest.main()
