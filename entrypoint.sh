#!/bin/sh

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Start the server
echo "Starting the server..."
exec "$@"
