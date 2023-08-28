#!/bin/bash
set -e

function database_exists() {
    psql -t -c "SELECT 1 FROM pg_database WHERE datname='$1'" | grep -q 1 || return 1
    return 0
}

# Check if main database exists
if ! database_exists $POSTGRES_DB; then
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<EOSQL
        CREATE DATABASE $POSTGRES_DB;
EOSQL
fi

# Check if test database exists
if ! database_exists $TEST_DATABASE_NAME; then
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<EOSQL
        CREATE DATABASE $TEST_DATABASE_NAME;
EOSQL
fi
