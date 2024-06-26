import tqdm
import time
import pandas as pd
import os
from faker import Faker
import base64
import uuid
import grpc
from localsearch_grpc import localsearch_pb2
from localsearch_grpc import localsearch_pb2_grpc

def main():
    host = os.environ.get('LOCALSEARCH_SERVER', 'localhost')
    channel = grpc.insecure_channel(f'{host}:50051')
    stub = localsearch_pb2_grpc.LocalsearchStub(channel)

    query = input("Enter a query: ")
    res = stub.Query(localsearch_pb2.QueryRequest(
        request_id = str(uuid.uuid4()),
        query = query
    ))

    for ds in res.document_scores:
        print(f'  {ds.document_id} - {ds.score}')

if __name__ == '__main__':
    main()