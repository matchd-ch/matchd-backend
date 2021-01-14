#!/bin/bash
set -e

echo "HOST: ${DJANGO_DB_HOST}";
echo "DATABASE: ${DJANGO_DB_PORT}";

# Check if script was called by CMD, can be sh -c 'CMD' or CMD
if [ "$1" = '/usr/libexec/s2i/run' ] || [ "$3" = '/usr/libexec/s2i/run' ] || [ "$2" = 'runserver' ]; then
    # Wait for the database to be available
    # until nc -vzw 2 $DJANGO_DB_HOST $DJANGO_DB_PORT; do echo "mysql is not available. waiting..." && sleep 2; done

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
fi

exec "$@"
