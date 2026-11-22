import json
import unittest
from io import BytesIO

import socket
import threading
import urllib.request

from wsgiref.simple_server import make_server

from app import (
    ThreadingWSGIServer,
    TimeoutRequestHandler,
    application,
    create_server,
)


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


class ConnectionHandlingTests(unittest.TestCase):
    def test_idle_connection_does_not_block_requests(self):
        server = create_server("127.0.0.1", 0)
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        idle = socket.create_connection(("127.0.0.1", port))
        try:
            with urllib.request.urlopen(
                "http://127.0.0.1:%d/health" % port, timeout=5
            ) as response:
                self.assertEqual(response.status, 200)
        finally:
            idle.close()
            server.shutdown()
            server.server_close()

    def test_idle_connection_is_closed_after_timeout(self):
        class ShortTimeoutHandler(TimeoutRequestHandler):
            timeout = 0.5

        server = make_server(
            "127.0.0.1",
            0,
            application,
            server_class=ThreadingWSGIServer,
            handler_class=ShortTimeoutHandler,
        )
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        idle = socket.create_connection(("127.0.0.1", port))
        try:
            idle.settimeout(5)
            # The server closes the idle socket (EOF) once its timeout fires,
            # well before our longer client-side timeout.
            self.assertEqual(idle.recv(1), b"")
        finally:
            idle.close()
            server.shutdown()
            server.server_close()

    def test_partial_request_timeout_is_dropped_quietly(self):
        class ShortTimeoutHandler(TimeoutRequestHandler):
            timeout = 0.5

        server = make_server(
            "127.0.0.1",
            0,
            application,
            server_class=ThreadingWSGIServer,
            handler_class=ShortTimeoutHandler,
        )
        errors = []
        server.handle_error = lambda request, client_address: errors.append(
            client_address
        )
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        partial = socket.create_connection(("127.0.0.1", port))
        try:
            partial.settimeout(5)
            partial.sendall(b"GET /health HTTP/1.1\r\nHost: x\r\n")
            self.assertEqual(partial.recv(1), b"")
            self.assertEqual(errors, [])
        finally:
            partial.close()
            server.shutdown()
            server.server_close()

    def test_environ_reports_multithread(self):
        seen = {}

        def capture(environ, start_response):
            seen["multithread"] = environ["wsgi.multithread"]
            start_response("200 OK", [("Content-Length", "0")])
            return []

        server = create_server("127.0.0.1", 0)
        server.set_app(capture)
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            urllib.request.urlopen(
                "http://127.0.0.1:%d/" % port, timeout=5
            ).close()
        finally:
            server.shutdown()
            server.server_close()
        self.assertTrue(seen["multithread"])


if __name__ == "__main__":
    unittest.main()
