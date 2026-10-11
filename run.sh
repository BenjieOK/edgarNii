#!/bin/bash
set -e
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."
#python manage.py collectstatic --noinput

echo "Starting Django with Gunicorn..."
gunicorn config.wsgi:application