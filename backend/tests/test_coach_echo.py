import unittest

from fastapi.testclient import TestClient

from app.main import create_app


class CoachEchoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())

    def test_echo_accepts_manual_paste(self) -> None:
        response = self.client.post(
            "/api/v1/coach/echo",
            json={
                "mode": "explain_code",
                "source": "manual_paste",
                "content": "counts[num] = counts.get(num, 0) + 1",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["mode"], "explain_code")
        self.assertEqual(response.json()["source"], "manual_paste")
        self.assertEqual(response.json()["content_length"], 36)

    def test_echo_rejects_empty_content(self) -> None:
        response = self.client.post(
            "/api/v1/coach/echo",
            json={"mode": "manual", "source": "manual_paste", "content": ""},
        )

        self.assertEqual(response.status_code, 422)

    def test_echo_rejects_unknown_source(self) -> None:
        response = self.client.post(
            "/api/v1/coach/echo",
            json={"mode": "manual", "source": "page_scrape", "content": "text"},
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
