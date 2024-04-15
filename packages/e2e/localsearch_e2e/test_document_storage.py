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
    contents_bytes = contents.encode("utf-8")
    contents_base64 = base64.b64encode(contents_bytes).decode('utf-8')

    return document_id, contents_base64


def test_insert_document():
    # Given we are connected to the GRPC server
    stub = connect_grpc()
    
    # When we call InsertDocument()
    request_id = str(uuid.uuid4())
    document_id, contents_base64 = generate_document()

    res = stub.InsertDocument(localsearch_pb2.InsertDocumentRequest(
        request_id = request_id,
        document_id = document_id,
        contents_base64 = contents_base64
    ))

    # Then we get a success response
    assert res.request_id == request_id
    assert res.response_code == 0

def test_get_document():
    # Given we are connected to the GRPC server
    stub = connect_grpc()

    # Given a document has been inserted
    document_id, contents_base64 = generate_document()
    stub.InsertDocument(localsearch_pb2.InsertDocumentRequest(
        request_id = str(uuid.uuid4()),
        document_id = document_id,
        contents_base64 = contents_base64
    ))
    
    # When we call GetDocument()
    request_id = str(uuid.uuid4())
    res = stub.GetDocument(localsearch_pb2.GetDocumentRequest(
        request_id = request_id,
        document_id = document_id
    ))

    # Then we get the same document contents as we inserted
    assert res.request_id == request_id
    assert res.response_code == 0
    assert res.contents_base64 == contents_base64



def test_query():
    # Given we are connected to the GRPC server
    stub = connect_grpc()

    # Given we have inserted a document
    document_id, contents_base64 = generate_document()
    stub.InsertDocument(localsearch_pb2.InsertDocumentRequest(
        request_id = str(uuid.uuid4()),
        document_id = document_id,
        contents_base64 = contents_base64
    ))

    # When we make a query request
    request_id = str(uuid.uuid4())
    query = "hello"
    req = localsearch_pb2.QueryRequest(
        request_id = request_id,
        query = query
    )
    res = stub.Query(req)

    # Then that document is in the response, and has a score
    assert res.request_id == req.request_id
    assert res.response_code == 0
    found = False
    for ds in res.document_scores: 
        if ds.document_id == document_id:
            found = True
            break
    assert found == True
