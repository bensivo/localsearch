import base64
import random
import asyncio
from concurrent import futures
import grpc
import logging
import localsearch_pb2_grpc
import localsearch_pb2

import tokenization

def b64decode(s):
    s_bytes = s.encode("utf-8")
    return base64.b64decode(s_bytes).decode('utf-8')

class LocalsearchServicer(localsearch_pb2_grpc.LocalsearchServicer):
    """
    Implements the LocalsearchService grpc service
    """
    async def InsertDocument(self, request, context):
        logging.info(f'->REQ InsertDocument:{request.request_id}')

        await asyncio.sleep(random.random())

        content = b64decode(request.contents_base64)
        tokens = tokenization.tokenize(content)
        logging.debug(f'Tokens: {tokens}')

        res = localsearch_pb2.InsertDocumentResponse(
            request_id = request.request_id,
            response_code = 0,
        )
        logging.info(f'<-RES InsertDocument:{res.request_id} - {res.response_code}')
        return res

async def serve():
    logging.info(f'Downloading tokenization data')
    tokenization.init_tokenization()

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    localsearch_pb2_grpc.add_LocalsearchServicer_to_server(
        LocalsearchServicer(), 
        server
    )
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.get_event_loop().run_until_complete(
        serve()
    )