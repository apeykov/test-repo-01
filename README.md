# test-repo-01

## Example Python web app

This repository contains a small web application built with Python's standard
library, so it has no external dependencies.

Start it with:

```bash
python app.py
```

Then open <http://127.0.0.1:8000> in a browser. The `/health` endpoint returns
JSON and can be used to check that the application is running.
The `/about` page describes the application.

Run the tests with:

```bash
python -m unittest -v
```