#!/bin/sh
set -e

echo "Waiting for postgres..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "Waiting for redis..."
while ! nc -z "$REDIS_HOST" "$REDIS_PORT"; do
  sleep 1
done

echo "Running migrations..."
python manage.py migrate

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000