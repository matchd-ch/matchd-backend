#!/bin/sh

set -eux

if [ "${RESET_DB:-true}" = "true" ]; then
    echo "Reset DB"
    DB_NAME_BEFORE="$DB_NAME"
    (
        export DB_NAME=mysql
        echo "DROP DATABASE IF EXISTS \`${DB_NAME_BEFORE}\`;" | ./manage.py dbshell
        echo "CREATE DATABASE \`${DB_NAME_BEFORE}\`;" | ./manage.py dbshell
    )
fi

if [ -w "static" ]; then
    echo "Collect static files"
    python ./manage.py collectstatic --noinput
else
    echo "static not writable, skipping collectstatic"
fi

if [ "${SETUP_DB:-true}" = "true" ]; then
    echo "Apply database migrations"
    python ./manage.py migrate

    echo "Load initial data"
    ./manage.py load_initial_data

    if [ "${RESET_DB:-true}" = "true" ]; then
        ./manage.py loaddata db/fixtures/initial_data.json
    fi

    echo "Load fallback images"
    ./manage.py load_media

    echo "Load test data"
    ./manage.py seed

    echo "Reindex elastic"
    python ./manage.py update_index
fi