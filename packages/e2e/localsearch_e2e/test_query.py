import os
from faker import Faker
import base64
import uuid
import grpc
from localsearch_grpc import localsearch_pb2
from localsearch_grpc import localsearch_pb2_grpc

fake = Faker()

def connect_grpc():
    host = os.environ['LOCALSEARCH_SERVER']
    channel = grpc.insecure_channel(f'{host}:50051')
    stub = localsearch_pb2_grpc.LocalsearchStub(channel)
    return stub

def generate_document():
    document_id = fake.isbn10()
    contents = fake.text()

    return document_id, contents

def insert_document(stub, document_id, contents):
    contents_bytes = contents.encode("utf-8")
    contents_base64 = base64.b64encode(contents_bytes).decode('utf-8')

    stub.InsertDocument(localsearch_pb2.InsertDocumentRequest(
        request_id = str(uuid.uuid4()),
        document_id = document_id,
        contents_base64 = contents_base64,
    ))

def test_query():
    # Given we're connected
    stub = connect_grpc()

    # Given we have 2 documents inserted
    doc1_id = fake.isbn10()
    doc1_contents = "Hello, world! It's a beautiful day today, isn't it?"

    doc2_id = fake.isbn10()
    doc2_contents = "Goodbye, cruel world. It's kind of a bummer today, isn't it?"

    insert_document(stub, doc1_id, doc1_contents)
    insert_document(stub, doc2_id, doc2_contents)

    # When we query, with the text from document 1
    res = stub.Query(localsearch_pb2.QueryRequest(
        request_id = str(uuid.uuid4()),
        query = "hello world beautiful day"
    ))

    # Then document 1 has a higher score than document 2
    score_doc1 = 0
    score_doc2 = 0

    for ds in res.document_scores:
        if ds.document_id == doc1_id:
            score_doc1 = ds.score
        if ds.document_id == doc2_id:
            score_doc2 = ds.score
    
    assert score_doc1 > score_doc2