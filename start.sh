#!/bin/sh

echo " Waiting for Postgres to be ready..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Postgres is up - running migrations"
alembic upgrade head

echo "Starting FastAPI app"
exec uvicorn main:app --host 0.0.0.0 --port 8000