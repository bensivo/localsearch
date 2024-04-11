from abc import ABC, abstractmethod
from concurrent import futures
from tokenization import Tokenizer
from document_store import DocumentStore
from utils import b64decode
import random
import grpc
import localsearch_pb2
import localsearch_pb2_grpc
import logging

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

    def __init__(self, port: int, tokenizer: Tokenizer, document_store: DocumentStore):
        self.port = port
        self.tokenizer = tokenizer
        self.document_store = document_store

    async def InsertDocument(self, request, context):
        """
        Implements the LocalsearchService grpc service
        """
        logging.info(f'->REQ InsertDocument:{request.request_id}')

        content = b64decode(request.contents_base64)

        logging.info(f'Saving document: {request.document_id}')
        self.document_store.save(request.document_id, content)

        tokens = self.tokenizer.tokenize(content)
        logging.debug(f'Tokens for document {request.document_id}: {tokens}')

        res = localsearch_pb2.InsertDocumentResponse(
            request_id = request.request_id,
            response_code = 0,
        )
        logging.info(f'<-RES InsertDocument:{res.request_id} - {res.response_code}')
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
