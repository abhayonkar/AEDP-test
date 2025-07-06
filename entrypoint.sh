#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Run database migrations
echo "Applying database migrations..."
python3 manage.py migrate

# Start the Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn aedp_project.wsgi:application --bind 0.0.0.0:10000
