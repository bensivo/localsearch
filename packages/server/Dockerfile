FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY ./dist/* /dist/

# Install the grpc dependency
# 
# Using .tar.gz files instead of .whl files preserves our local editable installs, and makes it easier to work between multiple platforms
RUN tar -xvzf /dist/localsearch_grpc-0.0.1.tar.gz  -C /app && mv /app/localsearch_grpc-0.0.1 /app/grpc-python
RUN cd /app/grpc-python && poetry install

# Install the server
# 
# Using .tar.gz files instead of .whl files preserves our local editable installs, and makes it easier to work between multiple platforms
RUN tar -xvzf /dist/localsearch_server-0.0.1.tar.gz  -C /app && mv /app/localsearch_server-0.0.1 /app/server
RUN cd /app/server && poetry install

EXPOSE 50051

CMD ["poetry", "--directory", "/app/server", "run", "python", "/app/server/localsearch_server/main.py"]