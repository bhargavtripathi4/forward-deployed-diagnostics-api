import unittest
from app import app

class DiagnosticsApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_status_endpoint(self):
        response = self.client.get("/status")
        self.assertEqual(response.status_code, 200)
        self.assertIn("uptime_seconds", response.get_json())

    def test_echo_accepts_valid_json(self):
        response = self.client.post("/diagnostics/echo", json={"message": "hello"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "hello")

    def test_echo_rejects_missing_message(self):
        response = self.client.post("/diagnostics/echo", json={})
        self.assertEqual(response.status_code, 400)

    def test_unknown_route_returns_json_404(self):
        response = self.client.get("/does-not-exist")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

if __name__ == "__main__":
    unittest.main()
