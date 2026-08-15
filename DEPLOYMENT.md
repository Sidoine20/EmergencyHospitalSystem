# Deployment Guide

This project is a Flask web app served by Waitress through `wsgi.py`.

## Recommended Beginner Deployment: Render

Render is a good first deployment target for this project because it can connect directly to GitHub, install `requirements.txt`, and run the Waitress start command without Docker knowledge.

Important database note: the app currently uses SQLite. On Render's free web service, local files are not a good place for permanent production data. This is acceptable for a class/demo deployment because the app seeds sample patients automatically. For real patient data, use a persistent disk or move to PostgreSQL before using it seriously.

## Files Used For Deployment

- `wsgi.py`: exposes the Flask app as `app`, which production servers use.
- `requirements.txt`: lists the Python packages Render installs.
- `Procfile`: start command for Heroku-style platforms.
- `render.yaml`: optional Render blueprint with build/start settings.
- `runtime.txt`: requests Python 3.11.9.
- `.env.example`: shows the environment variables to set.
- `Dockerfile`: optional container deployment path.

## Render Setup

1. Push this repository to GitHub.
2. Go to Render and create a new Web Service.
3. Connect `https://github.com/Sidoine20/EmergencyHospitalSystem`.
4. Use these settings:
   - Runtime: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m waitress --host=0.0.0.0 --port=$PORT --threads=8 wsgi:app`
   - Python Version: `3.11.9`
5. Add environment variables:
   - `SECRET_KEY`: a long random value used by Flask sessions and flash messages.
   - `DATABASE_PATH`: `hospital.db` for demo use.
6. Deploy the service.

## Start Command Explained

```bash
python -m waitress --host=0.0.0.0 --port=$PORT --threads=8 wsgi:app
```

- `python -m waitress`: runs the app with the installed Waitress production WSGI server.
- `--host=0.0.0.0`: accepts traffic from outside the container.
- `--port=$PORT`: uses the port assigned by the cloud platform.
- `--threads=8`: allows multiple requests at once.
- `wsgi:app`: loads `app` from `wsgi.py`.

## Environment Variables

| Variable | Purpose | Example |
|---|---|---|
| `SECRET_KEY` | Protects Flask sessions and flash messages | `generate-a-long-random-value` |
| `DATABASE_PATH` | SQLite database file path | `hospital.db` |

## Database Options

For a demo:

```text
DATABASE_PATH=hospital.db
```

For a paid Render persistent disk, mount a disk and set:

```text
DATABASE_PATH=/var/data/hospital.db
```

For a serious production version, migrate the SQLite layer to PostgreSQL so data survives deploys and supports concurrent access better.

## Local Production Test

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the same style of server used in production:

```bash
python -m waitress --host=0.0.0.0 --port=5000 --threads=8 wsgi:app
```

Then open:

```text
http://127.0.0.1:5000/
```
