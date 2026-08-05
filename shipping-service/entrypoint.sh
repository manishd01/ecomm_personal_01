#!/bin/sh

echo "Waiting for MySQL..."

while ! nc -z mysql 3306; do
  sleep 2
done

echo "MySQL is ready!"

echo "Running shipping migrations..."

alembic upgrade head

echo "Starting Shipping API on port 8000..."

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload