#!/bin/bash
set -e

echo "Apply database migrations"
python ./manage.py migrate

echo "Collect static files"
python ./manage.py collectstatic --noinput

echo "Setup super admin"
./manage.py loaddata app/fixtures/users.json

# Wait for elastic search to be available
until curl -s $DJANGO_ELASTIC_SEARCH_URL/_cluster/health | egrep '(green|yellow)' -i > /dev/null; do echo "elastic is not ready. waiting..." && sleep 5; done

#    TODO add initial data
#    echo "Load Demo data"
#    ./manage.py loaddata db/fixtures/initial_data.json
#
#    echo "Reindex elastic"
#    python ./manage.py update_index


exec "$@"
