#!/bin/bash
set -e

# Check if script was called by CMD, can be sh -c 'CMD' or CMD
if [ "$1" = '/usr/libexec/s2i/run' ] || [ "$3" = '/usr/libexec/s2i/run' ] || [ "$2" = 'runserver' ]; then
    echo "Apply database migrations"
    python ./manage.py migrate

    echo "Collect static files"
    python ./manage.py collectstatic --noinput

    echo "Reindex elastic"
    python ./manage.py update_index
fi

exec "$@"
