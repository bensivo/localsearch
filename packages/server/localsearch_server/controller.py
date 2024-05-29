import time
from abc import ABC, abstractmethod
from concurrent import futures
import grpc
import logging
import numpy as np
import random

from localsearch_grpc import localsearch_pb2
from localsearch_grpc import localsearch_pb2_grpc
from localsearch_server.service import LocalsearchService
from localsearch_server.utils import b64decode, b64encode


class Controller(ABC):
    """
    Controller is any class which exposes this application's functionality to the outside world.

    For example, using a GRPC server, an HTTP server, or a command-line interface.
    """
    @abstractmethod
    async def start(self):
        pass

class GrpcController(Controller, localsearch_pb2_grpc.LocalsearchServicer):
    """
    Exposes localsearch functions via a GRPC server
    """
    def __init__(self, port: int, service: LocalsearchService):
        self.port = port
        self.service = service

    async def InsertDocument(self, request, context):
        """
        Insert a document into the store, and the index
        """
        logging.info(f'->REQ InsertDocument:{request.request_id}')

        content = b64decode(request.contents_base64)
        self.service.insert_document(request.document_id, content)

        res = localsearch_pb2.InsertDocumentResponse(
            request_id = request.request_id,
            response_code = 0,
        )
        logging.info(f'<-RES InsertDocument:{res.request_id} - {res.response_code}')
        return res
    
    async def ListDocuments(self, request, context):
        """
        Return a list of all documents
        """
        logging.info(f'->REQ ListDocuments:{request.request_id}')

        document_ids = self.service.list_documents(request.limit, request.offset)
        documents_metadata = [localsearch_pb2.DocumentMetadata(
            document_id = document_id,
        ) for document_id in document_ids]

        res = localsearch_pb2.ListDocumentsResponse(
            request_id = request.request_id,
            response_code = 0,
            documents = documents_metadata
        )
        logging.info(f'<-RES ListDocuments:{res.request_id} - {res.response_code}')
        return res

    
    async def GetDocument(self, request, context):
        """
        Get a document from the store, returning the raw document contents as base64
        """
        logging.info(f'->REQ InsertDocument:{request.request_id}')

        content = self.service.get_document(request.document_id)

        if content is None:
            logging.warn(f'Document not found: {request.document_id}')
            res = localsearch_pb2.GetDocumentResponse(
                request_id = request.request_id,
                response_code = 1,
                contents_base64='',
            )
        else:
            logging.info(f'Document: {request.document_id} fetched successfully')
            res = localsearch_pb2.GetDocumentResponse(
                request_id = request.request_id,
                response_code = 0,
                contents_base64=b64encode(content),
            )
        logging.info(f'<-RES InsertDocument:{res.request_id} - {res.response_code} {res.contents_base64}')
        return res
    
    async def Index(self, request, context):
        logging.info(f'->REQ Index:{request.request_id}')

        index_res = self.service.index()

        res = localsearch_pb2.IndexResponse(
            request_id = request.request_id,
            response_code = 0,
        )
        logging.info(f'<-RES Index:{res.request_id} - {res.response_code}')
        return res
    
    async def Query(self, request, context):
        logging.info(f'->REQ Query:{request.request_id} "{request.query}"')

        query_res = self.service.query(request.query)

        document_scores = []
        for ds in query_res:
            print(ds['document_id'], ds['score'])
            document_scores.append(localsearch_pb2.DocumentScore(
                document_id = ds['document_id'],
                score = ds['score'],
            ))

        res = localsearch_pb2.QueryResponse(
            request_id = request.request_id,
            response_code = 0,
            document_scores = document_scores
        )
        logging.info(f'<-RES Query:{res.request_id} - {res.response_code}')
        return res


    async def start(self):
        server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
        localsearch_pb2_grpc.add_LocalsearchServicer_to_server(
            self, 
            server
        )
        server.add_insecure_port(f"[::]:{self.port}")
        await server.start()
        await server.wait_for_termination()
