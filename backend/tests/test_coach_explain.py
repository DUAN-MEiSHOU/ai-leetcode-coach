import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


class CoachExplainRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        get_settings.cache_clear()
        self.client = TestClient(create_app())

    def tearDown(self) -> None:
        get_settings.cache_clear()

    def test_explain_returns_503_without_api_key(self) -> None:
        with patch.dict("os.environ", {"DEEPSEEK_API_KEY": ""}):
            get_settings.cache_clear()
            response = self.client.post(
                "/api/v1/coach/explain",
                json={
                    "mode": "explain_code",
                    "source": "manual_paste",
                    "content": "return nums[i]",
                    "language": "python",
                },
            )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "DEEPSEEK_API_KEY is not configured.")

    def test_explain_rejects_unsupported_language(self) -> None:
        response = self.client.post(
            "/api/v1/coach/explain",
            json={
                "mode": "explain_code",
                "source": "manual_paste",
                "content": "return value",
                "language": "java",
            },
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
