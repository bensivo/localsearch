#!/bin/bash

until nc -w 1 $LOCALSEARCH_SERVER 50051; do echo "Waiting for server ${LOCALSEARCH_SERVER}:50010..."; sleep 1; done

exec poetry run pytest