#!/bin/bash

poetry run alembic upgrade head
cd ./app
poetry run uvicorn main:app --host 0.0.0.0 --reload --port 8000