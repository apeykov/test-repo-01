"""Small example web application using only Python's standard library."""

import json
from wsgiref.simple_server import make_server


STYLE = """
    :root {
      --bg: #f5f7fb; --card: #ffffff; --text: #1e2433; --muted: #5f6b85;
      --accent: #5b5bf0; --accent-2: #8b5cf6; --border: #e3e7f0;
      --shadow: 0 10px 30px rgba(30, 36, 51, .08);
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #0f1220; --card: #181c30; --text: #eef0f8; --muted: #9aa5c4;
        --border: #272d48; --shadow: 0 10px 30px rgba(0, 0, 0, .4);
      }
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; min-height: 100vh; display: flex; flex-direction: column;
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
      background: var(--bg); color: var(--text); line-height: 1.6;
    }
    header {
      background: var(--card); border-bottom: 1px solid var(--border);
      position: sticky; top: 0; z-index: 10;
    }
    nav {
      max-width: 960px; margin: 0 auto; padding: 14px 20px;
      display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
    }
    .brand {
      font-weight: 800; font-size: 1.15rem; margin-right: auto;
      background: linear-gradient(90deg, var(--accent), var(--accent-2));
      -webkit-background-clip: text; background-clip: text; color: transparent;
      text-decoration: none;
    }
    nav a.link {
      color: var(--muted); text-decoration: none; padding: 8px 14px;
      border-radius: 999px; font-weight: 500; transition: .2s;
    }
    nav a.link:hover { color: var(--accent); background: rgba(91, 91, 240, .1); }
    nav a.link.active { color: #fff; background: var(--accent); }
    main { flex: 1; width: 100%; max-width: 960px; margin: 0 auto; padding: 40px 20px; }
    .hero {
      text-align: center; padding: 56px 24px; border-radius: 24px; color: #fff;
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      box-shadow: var(--shadow);
    }
    .hero h1 { font-size: clamp(2rem, 6vw, 3.2rem); margin: 0 0 12px; }
    .hero p { font-size: 1.15rem; margin: 0 auto; max-width: 520px; opacity: .92; }
    .grid {
      display: grid; gap: 20px; margin-top: 32px;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    }
    .card {
      background: var(--card); border: 1px solid var(--border); border-radius: 18px;
      padding: 24px; box-shadow: var(--shadow); text-decoration: none; color: inherit;
      transition: transform .2s, border-color .2s;
    }
    a.card:hover { transform: translateY(-4px); border-color: var(--accent); }
    .card h2 { margin: 0 0 6px; font-size: 1.15rem; }
    .card p { margin: 0; color: var(--muted); }
    .card .icon { font-size: 1.8rem; display: block; margin-bottom: 10px; }
    h1 { margin-top: 0; }
    .panel {
      background: var(--card); border: 1px solid var(--border); border-radius: 20px;
      padding: 32px; box-shadow: var(--shadow);
    }
    .notice {
      background: rgba(91, 91, 240, .1); color: var(--accent);
      padding: 10px 16px; border-radius: 12px; font-weight: 500;
    }
    label { font-weight: 600; font-size: .92rem; }
    input, textarea {
      width: 100%; margin-top: 6px; padding: 12px 14px; font: inherit;
      color: var(--text); background: var(--bg);
      border: 1px solid var(--border); border-radius: 12px;
    }
    textarea { min-height: 130px; resize: vertical; }
    fieldset { border: 0; padding: 0; margin: 0; }
    fieldset:disabled { opacity: .6; }
    button {
      font: inherit; font-weight: 600; color: #fff; border: 0; cursor: pointer;
      padding: 12px 26px; border-radius: 999px;
      background: linear-gradient(90deg, var(--accent), var(--accent-2));
    }
    button:disabled { cursor: not-allowed; }
    .back { display: inline-block; margin-top: 20px; color: var(--accent); font-weight: 600; text-decoration: none; }
    .back:hover { text-decoration: underline; }
    footer { text-align: center; color: var(--muted); padding: 24px; font-size: .9rem; }
"""

NAV_ITEMS = [("/", "Home"), ("/about", "About"), ("/contact", "Contact")]


def render_page(title, content, active):
    """Wrap page content in the shared layout (header, navigation, footer)."""
    links = "".join(
        '<a class="link{}" href="{}">{}</a>'.format(
            " active" if href == active else "", href, label
        )
        for href, label in NAV_ITEMS
    )
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>{style}</style>
  </head>
  <body>
    <header>
      <nav>
        <a class="brand" href="/">Python demo app</a>
        {links}
      </nav>
    </header>
    <main>
{content}
    </main>
    <footer>Built with Python's standard library</footer>
  </body>
</html>
""".format(title=title, style=STYLE, links=links, content=content)


HTML_PAGE = render_page(
    "Python demo app",
    """      <section class="hero">
        <h1>Hello from Python!</h1>
        <p>This is a small example web application.</p>
      </section>
      <section class="grid">
        <a class="card" href="/about">
          <span class="icon">&#128214;</span>
          <h2>About</h2>
          <p>Learn more about this application.</p>
        </a>
        <a class="card" href="/contact">
          <span class="icon">&#9993;&#65039;</span>
          <h2>Contact Us</h2>
          <p>Get in touch with us.</p>
        </a>
        <a class="card" href="/health">
          <span class="icon">&#128154;</span>
          <h2>Check application health</h2>
          <p>See the live status of the app.</p>
        </a>
      </section>""",
    "/",
)

ABOUT_PAGE = render_page(
    "About - Python demo app",
    """      <div class="panel">
        <h1>About</h1>
        <p>This is a small example web application built with Python's standard library.</p>
        <a class="back" href="/">&larr; Back to home</a>
      </div>""",
    "/about",
)

CONTACT_PAGE = render_page(
    "Contact Us - Python demo app",
    """      <div class="panel">
        <h1>Contact Us</h1>
        <p class="notice">Message submission is not available yet.</p>
        <form>
          <fieldset disabled>
            <p><label for="name">Name</label><br><input id="name" name="name" type="text"></p>
            <p><label for="email">Email</label><br><input id="email" name="email" type="email"></p>
            <p><label for="message">Message</label><br><textarea id="message" name="message"></textarea></p>
            <button type="submit">Send message</button>
          </fieldset>
        </form>
        <a class="back" href="/">&larr; Back to home</a>
      </div>""",
    "/contact",
)


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
