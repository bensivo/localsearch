from tqdm import tqdm
import pandas as pd
import os
import base64
import uuid
import grpc

from localsearch_grpc import localsearch_pb2
from localsearch_grpc import localsearch_pb2_grpc

def main():
    host = os.environ.get('LOCALSEARCH_SERVER', 'localhost')
    channel = grpc.insecure_channel(f'{host}:50051')
    stub = localsearch_pb2_grpc.LocalsearchStub(channel)

    # Read the parquet file using pandas
    df = pd.read_parquet('./data/train-00000-of-00002.parquet')

    # Loop through each row in the DataFrame
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc='Inserting documents'):
        document_id = str(uuid.uuid4())
        document_contents = row['text']

        contents_bytes = document_contents.encode("utf-8")
        contents_base64 = base64.b64encode(contents_bytes).decode('utf-8')

        stub.InsertDocument(localsearch_pb2.InsertDocumentRequest(
            request_id = str(uuid.uuid4()),
            document_id = document_id,
            contents_base64 = contents_base64,
        ))

    res = stub.Index(localsearch_pb2.IndexRequest(
        request_id = str(uuid.uuid4())
    ))

if __name__ == '__main__':
    main()