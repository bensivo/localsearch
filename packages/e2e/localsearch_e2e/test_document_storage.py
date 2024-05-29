import os
from faker import Faker
import base64
import uuid
import grpc

from localsearch_grpc import localsearch_pb2
from localsearch_grpc import localsearch_pb2_grpc

fake = Faker()

def connect_grpc():
    host = os.environ.get('LOCALSEARCH_SERVER', 'localhost')
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

def test_list_documents():
    # Given we are connected to the GRPC server
    stub = connect_grpc()
    
    # Given we have inserted a document
    request_id = str(uuid.uuid4())
    document_id, contents_base64 = generate_document()
    res = stub.InsertDocument(localsearch_pb2.InsertDocumentRequest(
        request_id = request_id,
        document_id = document_id,
        contents_base64 = contents_base64
    ))

    # When we call ListDocuments
    res = stub.ListDocuments(localsearch_pb2.ListDocumentsRequest(
        request_id = request_id,
        limit = 100,
        offset = 0,
    ))

    documents = res.documents
    document_ids = [doc.document_id for doc in documents]

    # Then we get our document_id back
    assert document_id in document_ids

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
