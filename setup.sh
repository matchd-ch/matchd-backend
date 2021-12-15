#!/bin/sh

set -eux

if [ "${RESET_DB:-true}" = "true" ]; then
    echo "Reset DB"
    (
        export DJANGO_DB_NAME=mysql
        echo "DROP DATABASE IF EXISTS matchd;" | ./manage.py dbshell
        echo "CREATE DATABASE matchd;" | ./manage.py dbshell
    )
fi

echo "Apply database migrations"
python ./manage.py migrate

echo "Collect static files"
python ./manage.py collectstatic --noinput

echo "Load initial data"
./manage.py load_initial_data
./manage.py loaddata db/fixtures/initial_data.json

echo "Load fallback images"
./manage.py load_media

echo "Load test data"
./manage.py seed

echo "Reindex elastic"
python ./manage.py update_index