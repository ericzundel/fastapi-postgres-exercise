# conftest.py
import pytest
import socket
import requests
import time

# Constants used in all integration tests
FASTAPI_URL = "http://localhost:8000"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432


@pytest.fixture(scope="session")
def config():
    """Provide shared config values for tests."""
    return {
        "fastapi_url": FASTAPI_URL,
        "postgres_host": POSTGRES_HOST,
        "postgres_port": POSTGRES_PORT,
    }

def wait_for_port(host, port, timeout=10):
    ''' Wait for a TCP port to become available. '''
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False

def wait_for_http(url, timeout=10):
    ''' Wait for an HTTP endpoint to respond with a non-500 status. '''
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code < 500:
                return True
        except Exception:
            time.sleep(0.5)
    return False

def pytest_sessionstart(session):
    """Called after the Session object has been created and before tests are collected."""
    print("🔍 Checking that services are up...")

    if not wait_for_port(POSTGRES_HOST, POSTGRES_PORT):
        pytest.exit("❌ Database not reachable on port 5432", returncode=1)

    if not wait_for_http(f"{FASTAPI_URL}/health"):
        pytest.exit("❌ HTTP service not responding at /health", returncode=1)

    print("✅ All services are running.")