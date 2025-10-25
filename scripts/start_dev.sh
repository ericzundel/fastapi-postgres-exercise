#!/usr/bin/env bash
# Script to run the service for a development environment

set -euo pipefail  # Exit on error, undefined vars, and pipeline failures

# Get the root of the workspace, ignoring $CWD
WORKSPACE_ROOT=$(dirname "$(realpath "$0")")/..

cd ${WORKSPACE_ROOT}
. venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
