"""Small example web application using only Python's standard library."""

import json
from wsgiref.simple_server import make_server


HTML_PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Python demo app</title>
  </head>
  <body>
    <main>
      <h1>Hello from Python!</h1>
      <p>This is a small example web application.</p>
      <p><a href="/health">Check application health</a></p>
    </main>
  </body>
</html>
"""


def application(environ, start_response):
    """Return a response for the requested path."""
    path = environ.get("PATH_INFO", "/")

    if path == "/":
        body = HTML_PAGE.encode("utf-8")
        status = "200 OK"
        content_type = "text/html; charset=utf-8"
    elif path == "/health":
        body = json.dumps({"status": "ok"}).encode("utf-8")
        status = "200 OK"
        content_type = "application/json"
    else:
        body = b"Not found"
        status = "404 Not Found"
        content_type = "text/plain; charset=utf-8"

    start_response(
        status,
        [
            ("Content-Type", content_type),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]


def create_server(host="127.0.0.1", port=8000):
    """Create the development server without starting it."""
    return make_server(host, port, application)


if __name__ == "__main__":
    print("Serving http://127.0.0.1:8000 (press Ctrl+C to stop)")
    create_server().serve_forever()
