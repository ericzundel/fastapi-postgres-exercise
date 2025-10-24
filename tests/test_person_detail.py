import types

import pytest
from fastapi.testclient import TestClient

import app.main as main

@pytest.fixture(autouse=True)
def disable_init_db(monkeypatch):
    """Prevent the real DB setup during tests by patching init_db to a no-op."""
    async def noop():
        return None

    monkeypatch.setattr(main, "init_db", noop)
    yield


def make_session_for(person):
    """Return a callable that creates an async context manager session which implements get()."""

    class DummySession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, model, id):
            return person if id == getattr(person, "id", None) else None

    return lambda: DummySession()


def test_read_person_found(monkeypatch):
    # Create a tiny, attribute-based object to stand in for a SQLAlchemy Person instance.
    # SimpleNamespace lets us reference .id, .first_name, etc., in templates and code under test
    # without importing or constructing a full ORM model.
    person = types.SimpleNamespace(id=1, first_name="Alice", last_name="Smith", email="a@example.com")
    # Patch the async_session used by the route to return our dummy session
    monkeypatch.setattr(main, "async_session", make_session_for(person))

    with TestClient(main.app) as client:
        res = client.get("/persons/1")

    assert res.status_code == 200
    assert "Alice" in res.text
    assert "a@example.com" in res.text


def test_read_person_not_found(monkeypatch):
    person = types.SimpleNamespace(id=1, first_name="Alice", last_name="Smith", email="a@example.com")
    monkeypatch.setattr(main, "async_session", make_session_for(person))

    with TestClient(main.app) as client:
        res = client.get("/persons/2")

    assert res.status_code == 404
    assert "404 Not Found" in res.text
