#!/bin/bash

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "$POSTGRES_USER" -tc "SELECT 1 FROM pg_database WHERE datname = 'sport_assistant'" | grep -q 1 || \
  PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "$POSTGRES_USER" -c "CREATE DATABASE sport_assistant"

poetry run alembic upgrade head
cd ./app
poetry run uvicorn main:app --host 0.0.0.0 --reload --port 8000