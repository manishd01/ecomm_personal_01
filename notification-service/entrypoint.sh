#!/bin/sh

echo "Waiting for MySQL..."

until nc -z $DB_HOST $DB_PORT; do
  echo "MySQL not ready, waiting..."
  sleep 2
done

echo "MySQL is ready!"

echo "Running notification migrations..."
alembic upgrade head

echo "Starting Notification API on port 8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
