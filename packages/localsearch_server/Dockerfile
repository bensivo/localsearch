FROM python:3.10-slim

WORKDIR /localsearch_server

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock ./
COPY ./deps/ ./deps/

RUN poetry install

COPY ./localsearch_server ./localsearch_server

EXPOSE 50051
CMD [ "poetry", "run", "python", "-m", "localsearch_server.main" ]
