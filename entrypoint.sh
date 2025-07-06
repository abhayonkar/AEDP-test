#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if the DJANGO_MANAGE_COMMAND variable is set
if [ -n "$DJANGO_MANAGE_COMMAND" ]; then
    # If it is set, run that command
    echo "Running Django management command: $DJANGO_MANAGE_COMMAND"
    python3 manage.py $DJANGO_MANAGE_COMMAND
else
    # Otherwise, start the web server as normal
    echo "Applying database migrations..."
    python3 manage.py migrate

    echo "Starting Gunicorn server..."
    exec gunicorn aedp_project.wsgi:application --bind 0.0.0.0:10000
fi
