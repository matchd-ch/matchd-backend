#!/bin/bash
set -e

echo "Apply database migrations"
python ./manage.py migrate

echo "Collect static files"
python ./manage.py collectstatic --noinput

echo "load data"
python ./manage.py load_initial_data

echo "Reindex elastic"
python ./manage.py update_index

exec "$@"
