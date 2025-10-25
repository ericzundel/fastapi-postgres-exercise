#!/usr/bin/env bash
#
# Library of shared functions for project management scripts
#

# Generate a random 10 character string using uuidgen
generate_random_string() {
    uuidgen | tr -d '-' | cut -c1-10
}

# Ensure we're running in bash
check_bash() {
    if [[ -z "$BASH_VERSION" ]]; then
        echo "Please run this script with bash"
        exit 1
    fi
}


# Prompt for yes/no with default no
# Usage: if prompt_yes_no "Are you sure?"; then ... fi
prompt_yes_no() {
    local prompt="$1"
    local answer

    # Add the [y/N] to the prompt if not already present
    if [[ ! "$prompt" =~ \[y/N\]$ ]]; then
        prompt="$prompt [y/N]"
    fi

    # Read the answer
    read -r -p "$prompt " answer

    # Convert answer to lowercase
    # answer=${answer,,} # Bash only
    answer=$(printf '%s' "$answer" | tr '[:upper:]' '[:lower:]')

    # Return true only for "y" or "yes"
    [[ "$answer" =~ ^y(es)?$ ]]
}

check_database_url() {
	if [  -z "${DATABASE_URL:-}" ] ; then
        	echo "DATABASE_URL wasn't setup in .env-local"
        	exit 1
	fi
}

get_db_username() {
	$(check_database_url)
 	echo "$DATABASE_URL" | sed -E 's|[a-z\+]+://([^:]+):([^@]+)@.*|\1|'
}

get_db_password() {
	$(check_database_url)
	echo "$DATABASE_URL" | sed -E 's|[a-z\+]+://([^:]+):([^@]+)@.*|\2|'
}

get_db_host_with_port() {
	$(check_database_url)
	echo "$DATABASE_URL" | sed -E 's|[a-z\+]+://([^:]+):([^@]+)@([^/]+)/(.*)$|\3|'

}

get_db_host() {
    host_with_port=$(get_db_host_with_port)
    # Split host and port
    echo "$host_with_port" | cut -d':' -f1
}

get_db_name() {
	$(check_database_url)
	echo "$DATABASE_URL" | sed -E 's|[a-z\+]+://([^:]+):([^@]+)@([^/]+)/(.*)$|\4|'
}