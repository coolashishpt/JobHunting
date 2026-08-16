#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start passed command (default is gunicorn via Dockerfile CMD)
exec "$@"
