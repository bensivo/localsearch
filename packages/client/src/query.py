import base64
import uuid
import asyncio
import logging
import grpc
import localsearch_pb2
import localsearch_pb2_grpc

async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = localsearch_pb2_grpc.LocalsearchStub(channel)

        query = input("Query: ")

        request_id = str(uuid.uuid4())

        logging.info(f'REQ-> Query:{request_id}')
        req = localsearch_pb2.QueryRequest(
            request_id = request_id,
            query = query,
        )
        res = await stub.Query(req)
        logging.info(f'RES<- Query:{res.request_id} {res.response_code}')

        for ds in res.document_scores:
            logging.info(f'Document: {ds.document_id} - Score: {ds.score}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.get_event_loop().run_until_complete(main())