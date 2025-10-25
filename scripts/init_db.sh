#!/usr/bin/env bash
# Script to add the database and setup a user from a fresh mysql install

set -euo pipefail  # Exit on error, undefined vars, and pipeline failures


# Get the root of the workspace, ignoring $CWD
WORKSPACE_ROOT=$(dirname "$(realpath "$0")")/..

# Source the shared libraries
source "${WORKSPACE_ROOT}/scripts/lib/cli_utils.sh"

if [ -f ${WORKSPACE_ROOT}/.env ] ; then
    # shellcheck disable=SC1091
    source "${WORKSPACE_ROOT}/.env"
else
    echo ".env file not found in project root"
fi

db_username=$(get_db_username)
db_password=$(get_db_password)
db_host=$(get_db_host)
db_name=$(get_db_name)

echo "Username: $db_username"
#echo "Password: $db_password"
echo "Host Name: $db_host"
echo "Database Name: $db_name"
echo

########################
set +e # Ignore errors for the next commands

CMD="create user ${db_username} with password '${db_password}'"
psql -h ${db_host} postgres -c "$CMD"
CMD="create database  ${db_name} owner ${db_username}"
psql -h ${db_host} postgres -c "$CMD"

set -e # Resume exit on error
########################

CMD="GRANT USAGE ON SCHEMA public TO ${db_username}"
psql -h ${db_host} postgres -c "$CMD"
CMD="GRANT CREATE ON SCHEMA public TO ${db_username}"
psql -h ${db_host} postgres -c "$CMD"