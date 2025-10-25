# fastapi-postgres-exercise

Small FastAPI example that stores a Person (id, first_name, last_name, email) into Postgres using async SQLAlchemy.

## Purpose

This is a project I used to learn more about writing a service using FastAPI.  I'm using it to make sure I understand how to use a database, run CI/CD, and use the builtin tools for exercising and documenting the JSON API.  I used an AI agent to assist.

## Quick start

### Prerequisites

Assumes you have a development environment on your system with the following installed:
- postgresql database (I used 14.19 installed with Homebrew)
- python3 (I used 3.9 installed with Homebrew)

### Installation instructions 

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy and set your database URL in `.env` (see `.env.example`):

```bash
cp .env.example .env
# edit .env to set your DATABASE_URL
```

### Running the app

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/ to see the form and insert a Person into the `person` table.

Notes

- The app uses an async SQLAlchemy engine and will create the `person` table at startup if it doesn't exist.
- The default DATABASE_URL in `.env.example` points to a local Postgres with user `postgres` and database `postgres` — change it for your environment.
