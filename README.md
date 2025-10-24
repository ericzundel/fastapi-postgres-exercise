# fastapi-postgres-exercise

Small FastAPI example that stores a Person (id, first_name, last_name, email) into Postgres using async SQLAlchemy.

Quick start

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

4. Run the app:

```bash
uvicorn app.main:app --reload
```

5. Open http://127.0.0.1:8000/ to see the form and insert a Person into the `person` table.

Notes

- The app uses an async SQLAlchemy engine and will create the `person` table at startup if it doesn't exist.
- The default DATABASE_URL in `.env.example` points to a local Postgres with user `postgres` and database `postgres` — change it for your environment.
# fastapi-postgres-exercise
