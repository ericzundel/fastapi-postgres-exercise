#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration tests for Person creation and retrieval.

Author: Eric Ayers
Created: 2025-10-24
Usage: Start Postgres and faexample as a service and run with pytest
"""
import re
import uuid
import pytest
from httpx import AsyncClient

from conftest import FASTAPI_URL

@pytest.mark.asyncio
async def test_create_and_get_person_json():
	"""Create a person via the JSON endpoint and then retrieve it.

	- POST JSON to {FASTAPI_URL}/persons/new with first_name, last_name, email
	- Expect a JSON response containing an `id` for the created person
	- GET {FASTAPI_URL}/persons/{id} and verify the stored fields
	"""

	suffix = uuid.uuid4().hex[:8]
	first = f"Integration{suffix}"
	last = "test"
	email = f"{first}@example.com"
	url = FASTAPI_URL
	create_url = f"{url}/persons/new"

	async with AsyncClient(base_url=url, timeout=10.0) as client:
		# Create the person via JSON
		res = await client.post(create_url, json={
			"first_name": first,
			"last_name": last,
			"email": email,
		})

		assert res.status_code in (200, 201), f"unexpected status: {res.status_code} - {res.text}"

		# Try parsing JSON response for created id
		person_id = None
		try:
			data = res.json()
			# common patterns: {"id": 1, ...} or {"person": {"id": 1, ...}}
			if isinstance(data, dict):
				if "id" in data:
					person_id = data["id"]
				elif "person" in data and isinstance(data["person"], dict) and "id" in data["person"]:
					person_id = data["person"]["id"]
		except ValueError:
			# not JSON — try extracting ID from HTML as a fallback
			m = re.search(r"ID:\s*(\d+)", res.text)
			if m:
				person_id = int(m.group(1))

		assert person_id is not None, f"Could not determine created person id from response: {res.text}"

		# Retrieve the person
		get_url = f"{url}/persons/{person_id}"
		res2 = await client.get(get_url)
		assert res2.status_code == 200, f"GET returned {res2.status_code}: {res2.text}"

		# Try to parse JSON body; fall back to HTML/text assertions
		try:
			data2 = res2.json()
			assert data2.get("first_name") == first
			assert data2.get("last_name") == last
			assert data2.get("email") == email
		except ValueError:
			# not JSON — assert the HTML contains the expected values
			assert first in res2.text
			assert last in res2.text
			assert email in res2.text

		# Best-effort cleanup: attempt HTTP DELETE if available; ignore errors
		try:
			await client.delete(get_url)
		except Exception:
			pass


