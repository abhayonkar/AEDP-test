#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if the DJANGO_MANAGE_COMMAND variable is set

    # Otherwise, start the web server as normal
echo "Applying database migrations..."
python3 manage.py migrate

echo "Starting Gunicorn server..."
exec gunicorn aedp_project.wsgi:application --bind 0.0.0.0:10000

