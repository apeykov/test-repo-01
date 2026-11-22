import json
import unittest
from io import BytesIO

from app import application


def request(path, method="GET"):
    environ = {
        "PATH_INFO": path,
        "REQUEST_METHOD": method,
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
        self.assertIn(b'href="/products"', response["body"])
        self.assertIn(b'href="/about"', response["body"])
        self.assertIn(b'href="/contact"', response["body"])

    def test_products_page(self):
        response = request("/products")

        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["headers"]["Content-Type"], "text/html; charset=utf-8")
        self.assertIn(b"<h1>Products</h1>", response["body"])
        self.assertIn(b"<h2>Starter Kit</h2>", response["body"])
        self.assertIn(b"<h2>Pro Toolkit</h2>", response["body"])
        self.assertIn(b"<h2>Enterprise Suite</h2>", response["body"])
        self.assertIn(b'aria-current="page"', response["body"])
        self.assertEqual(int(response["headers"]["Content-Length"]), len(response["body"]))

    def test_products_page_head(self):
        response = request("/products", method="HEAD")
        get_response = request("/products")

        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["headers"], get_response["headers"])
        self.assertEqual(response["body"], b"")

    def test_about_page(self):
        response = request("/about")

        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["headers"]["Content-Type"], "text/html; charset=utf-8")
        self.assertIn(b"<h1>About</h1>", response["body"])
        self.assertIn(b'href="/"', response["body"])
        self.assertEqual(int(response["headers"]["Content-Length"]), len(response["body"]))

    def test_about_page_head(self):
        response = request("/about", method="HEAD")
        get_response = request("/about")

        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["headers"], get_response["headers"])
        self.assertEqual(response["body"], b"")

    def test_contact_page(self):
        response = request("/contact")

        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["headers"]["Content-Type"], "text/html; charset=utf-8")
        self.assertIn(b"<h1>Contact Us</h1>", response["body"])
        self.assertIn(b"Message submission is not available yet.", response["body"])
        self.assertIn(b"<fieldset disabled>", response["body"])
        self.assertIn(b'href="/"', response["body"])
        self.assertEqual(int(response["headers"]["Content-Length"]), len(response["body"]))

    def test_contact_page_head(self):
        response = request("/contact", method="HEAD")
        get_response = request("/contact")

        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["headers"], get_response["headers"])
        self.assertEqual(response["body"], b"")

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
