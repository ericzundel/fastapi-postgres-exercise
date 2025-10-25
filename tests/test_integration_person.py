import re
import uuid
#import asyncio

import pytest
from httpx import AsyncClient, ASGITransport

import app.main as main
from app.db import async_session
from app.models import Person

# @pytest.mark.skip(reason="This test is can example of an integration test and will fail if postgres isn't running.")
@pytest.mark.asyncio
async def test_create_and_get_person():
    """Integration test: POST form to create a Person, then fetch by ID.

    This test assumes a Postgres instance is reachable using the project's
    DATABASE_URL. It posts form-encoded data to `/persons/new`, parses the
    returned HTML for the assigned ID, then GETs `/persons/{id}` and checks
    that the person's fields appear on the page. Finally it removes the
    created Person from the DB to avoid leaving test data behind.
    """

    unique = uuid.uuid4().hex[:8]
    first = "Integration"
    last = "Tester"
    email = f"integration-{unique}@example.com"

    transport = ASGITransport(app=main.app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create person via form POST
        res = await client.post("/persons/new", data={
            "first_name": first,
            "last_name": last,
            "email": email,
        })

        assert res.status_code == 200

        # Extract the created ID from the HTML response (form.html shows "ID: {id}")
        m = re.search(r"ID:\s*(\d+)", res.text)
        assert m, "response should include created person ID"
        person_id = int(m.group(1))

        # Fetch the person detail page
        res2 = await client.get(f"/persons/{person_id}")
        assert res2.status_code == 200
        assert first in res2.text
        assert last in res2.text
        assert email in res2.text

    # Cleanup using the project's async_session inside the same async test loop
    async with async_session() as session:
        obj = await session.get(Person, person_id)
        if obj:
            await session.delete(obj)
            await session.commit()
