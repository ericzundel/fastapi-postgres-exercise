"""Test bootstrap: ensure project root is on sys.path so tests can import `app`.

Pytest sometimes runs with a working directory that doesn't make the project package
importable. This file prepends the repository root to sys.path so tests can do
`import app` reliably.
"""
import os
import sys

HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
