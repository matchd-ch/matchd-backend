#!/bin/bash
set -e

echo "Apply database migrations"
python ./manage.py migrate

echo "Collect static files"
python ./manage.py collectstatic --noinput

echo "Reindex elastic"
python ./manage.py update_index

exec "$@"
