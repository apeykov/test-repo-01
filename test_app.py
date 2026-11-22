import json
import unittest
from io import BytesIO

from app import application


def request(path):
    environ = {
        "PATH_INFO": path,
        "REQUEST_METHOD": "GET",
        "wsgi.input": BytesIO(),
    }
    response = {}

    def start_response(status, headers):
        response["status"] = status
        response["headers"] = dict(headers)

    response["body"] = b"".join(application(environ, start_response))
    return response


class ApplicationTests(unittest.TestCase):
    def test_home_page(self):
        response = request("/")

        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["headers"]["Content-Type"], "text/html; charset=utf-8")
        self.assertIn(b"Hello from Python!", response["body"])

    def test_health_endpoint(self):
        response = request("/health")

        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(json.loads(response["body"]), {"status": "ok"})

    def test_unknown_path(self):
        response = request("/missing")

        self.assertEqual(response["status"], "404 Not Found")
        self.assertEqual(response["body"], b"Not found")


if __name__ == "__main__":
    unittest.main()
