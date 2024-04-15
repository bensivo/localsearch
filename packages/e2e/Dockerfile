FROM python:3.10-slim

WORKDIR /localsearch_e2e

RUN apt update && apt install -y netcat-openbsd
RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock ./
COPY ./deps/ ./deps/

RUN poetry install

COPY ./localsearch_e2e ./localsearch_e2e
COPY ./docker-entrypoint.sh ./

ENTRYPOINT [ "./docker-entrypoint.sh" ]
