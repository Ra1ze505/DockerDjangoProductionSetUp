#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi
source /src/venv/bin/activate
python manage.py migrate --noinput || exit 1
python manage.py collectstatic --noinput
exec "$@"