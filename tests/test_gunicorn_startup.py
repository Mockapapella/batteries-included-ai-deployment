import subprocess
import time
import unittest

import requests


class TestGunicornStartup(unittest.TestCase):
    server_process: subprocess.Popen | None = None  # Type annotation

    @classmethod
    def setUpClass(cls) -> None:
        """Start the server."""
        cls.server_process = subprocess.Popen(
            [
                "gunicorn",
                "main:app",
                "--worker-class",
                "uvicorn.workers.UvicornWorker",
                "--workers",
                "2",
                "--bind",
                "0.0.0.0:8000",
            ]
        )
        time.sleep(5)  # Wait for the server to start

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the server."""
        if cls.server_process:
            cls.server_process.terminate()
            cls.server_process.wait()

    def test_predict_endpoint(self) -> None:
        """Make a call to the prediction endpoint."""
        url = "http://localhost:8000/predict/"
        params = {"message": "This is a test message"}
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200, "Expected status code to be 200 OK")


if __name__ == "__main__":
    unittest.main()
