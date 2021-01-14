#!/bin/bash
set -e

echo "HOST: ${DJANGO_DB_HOST}";
echo "DATABASE: ${DJANGO_DB_PORT}";

# Check if script was called by CMD, can be sh -c 'CMD' or CMD
if [ "$1" = '/usr/libexec/s2i/run' ] || [ "$3" = '/usr/libexec/s2i/run' ] || [ "$2" = 'runserver' ]; then
    echo "Apply database migrations"
    python ./manage.py migrate

    echo "Collect static files"
    python ./manage.py collectstatic --noinput

    echo "Setup super admin"
    ./manage.py loaddata app/fixtures/users.json

#    TODO add initial data
#    echo "Load Demo data"
#    ./manage.py loaddata db/fixtures/initial_data.json
#
#    echo "Reindex elastic"
#    python ./manage.py update_index
fi

exec "$@"
