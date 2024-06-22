import subprocess
import time
import unittest
from typing import Dict
from typing import Union

import requests


class TestGunicornStartup(unittest.TestCase):
    server_process: subprocess.Popen | None = None

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

    def test_generate_endpoint(self) -> None:
        """Make a call to the text generation endpoint."""
        url = "http://0.0.0.0:8000/generate/"
        params: Dict[str, Union[str, int]] = {
            "prompt": "Once upon a time",
            "max_length": 50,
        }
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200, "Expected status code to be 200 OK")


if __name__ == "__main__":
    unittest.main()
