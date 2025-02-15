FROM python:3.11.5-slim
WORKDIR /backend
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    && apt-get clean
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root
COPY ./app ./app
EXPOSE 8000
CMD ["sh", "-c", "cd ./app && poetry run uvicorn main:app --host 0.0.0.0 --port 8000"]
