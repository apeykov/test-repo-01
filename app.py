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
      <p><a href="/about">About</a></p>
      <p><a href="/contact">Contact Us</a></p>
      <p><a href="/health">Check application health</a></p>
    </main>
  </body>
</html>
"""

ABOUT_PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>About - Python demo app</title>
  </head>
  <body>
    <main>
      <h1>About</h1>
      <p>This is a small example web application built with Python's standard library.</p>
      <p><a href="/">Back to home</a></p>
    </main>
  </body>
</html>
"""

CONTACT_PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Contact Us - Python demo app</title>
  </head>
  <body>
    <main>
      <h1>Contact Us</h1>
      <p>Message submission is not available yet.</p>
      <form>
        <fieldset disabled>
          <p><label for="name">Name</label><br><input id="name" name="name" type="text"></p>
          <p><label for="email">Email</label><br><input id="email" name="email" type="email"></p>
          <p><label for="message">Message</label><br><textarea id="message" name="message"></textarea></p>
          <button type="submit">Send message</button>
        </fieldset>
      </form>
      <p><a href="/">Back to home</a></p>
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
    elif path == "/about":
        body = ABOUT_PAGE.encode("utf-8")
        status = "200 OK"
        content_type = "text/html; charset=utf-8"
    elif path == "/contact":
        body = CONTACT_PAGE.encode("utf-8")
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
    return [] if environ.get("REQUEST_METHOD") == "HEAD" else [body]


def create_server(host="127.0.0.1", port=8000):
    """Create the development server without starting it."""
    return make_server(host, port, application)


if __name__ == "__main__":
    print("Serving http://127.0.0.1:8000 (press Ctrl+C to stop)")
    create_server().serve_forever()
