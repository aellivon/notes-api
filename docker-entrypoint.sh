#!/bin/bash

set -e

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate

echo "Starting server"
python manage.py runserver 0.0.0.0:8000