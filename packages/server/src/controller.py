from abc import ABC, abstractmethod
from concurrent import futures
from document_store import DocumentStore
from localsearch_grpc import localsearch_pb2
from localsearch_grpc import localsearch_pb2_grpc
from tf_index import TFIndex
from tokenizer import Tokenizer
from utils import b64decode, b64encode
import grpc
import logging
import numpy as np
import random


class Controller(ABC):
    """
    Controller is any class which exposes this application's functionality to the outside world.

    For example, using a GRPC server, an HTTP server, or a command-line interface.
    """

    @abstractmethod
    async def start(self):
        pass

# class GrpcController(Controller, localsearch_pb2_grpc.LocalsearchServicer):
class GrpcController(Controller, localsearch_pb2_grpc.LocalsearchServicer):
    """
    Exposes localsearch functions via a GRPC server
    """

    def __init__(self, port: int, tokenizer: Tokenizer, document_store: DocumentStore, tf_index: TFIndex):
        self.port = port
        self.tokenizer = tokenizer
        self.document_store = document_store
        self.tf_index = tf_index

    async def InsertDocument(self, request, context):
        """
        Insert a document into the store, and the index
        """
        logging.info(f'->REQ InsertDocument:{request.request_id}')

        content = b64decode(request.contents_base64)

        logging.info(f'Saving document: {request.document_id}')
        self.document_store.save(request.document_id, content)

        tf_dict = self.tokenizer.get_tf_dict(content)
        logging.debug(f'Tokens for document {request.document_id}: {tf_dict}')

        logging.info(f'Inserting tokens for document {request.document_id} into tf_index')
        for token in tf_dict:
            self.tf_index.save_term_frequency(token, request.document_id, tf_dict[token])

        logging.info(f'Terms: {self.tf_index.get_terms()}')
        logging.info(f'TF Vector: {self.tf_index.get_term_vector(request.document_id)}')

        res = localsearch_pb2.InsertDocumentResponse(
            request_id = request.request_id,
            response_code = 0,
        )
        logging.info(f'<-RES InsertDocument:{res.request_id} - {res.response_code}')
        return res
    
    async def GetDocument(self, request, context):
        """
        Get a document from the store, returning the raw document contents as base64
        """
        logging.info(f'->REQ InsertDocument:{request.request_id}')

        logging.info(f'Getting document: {request.document_id}')
        content = self.document_store.get(request.document_id)

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
    
    async def Query(self, request, context):
        logging.info(f'->REQ Query:{request.request_id}')

        # Calculate tf-vector for the query itself
        terms = self.tf_index.get_terms()
        query_terms = self.tokenizer.get_tf_dict(request.query)
        query_tf_vector = np.array([query_terms.get(term, 0) for term in terms])

        document_scores = []

        # Calculate tf-vectors for each document
        document_ids = self.document_store.list_documents()
        for document_id in document_ids:

            # Calculate similarity for each doc
            tf_vector = np.array(self.tf_index.get_term_vector(document_id))

            similarity = np.dot(query_tf_vector, tf_vector) / (np.linalg.norm(query_tf_vector) * np.linalg.norm(tf_vector))
            logging.debug(f'Cosine Similarity between query and {document_id}: {similarity}')

            document_scores.append(DocumentScore(
                document_id = document_id,
                score = similarity,
            ))

        # Sort by similarity, returning doc ids
        document_scores.sort(key=lambda x: x.score, reverse=True)

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
