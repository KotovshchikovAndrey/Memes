FROM python:3.11

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

COPY ./src ./src

RUN poetry config virtualenvs.create false && poetry install --only main
