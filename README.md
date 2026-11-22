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
The `/products` page displays a small demo product catalog.
The `/about` page describes the application.
The `/contact` page displays a contact form; message submission is not yet available.

Run the tests with:

```bash
python -m unittest -v
```