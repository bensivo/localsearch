import base64
import uuid
import asyncio
import logging
import grpc
import localsearch_pb2
import localsearch_pb2_grpc
from faker import Faker

fake = Faker()

def b64encode(s):
    s_bytes = s.encode("utf-8")
    return base64.b64encode(s_bytes).decode('utf-8')

async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = localsearch_pb2_grpc.LocalsearchStub(channel)

        request_id = str(uuid.uuid4())
        document_id = fake.isbn10()
        contents = fake.text()

        logging.info(f'REQ-> InsertDocument:{request_id} "{contents}"')
        req = localsearch_pb2.InsertDocumentRequest(
            request_id = request_id,
            document_id = document_id,
            contents_base64 = b64encode(contents),
        )
        res = await stub.InsertDocument(req)
        logging.info(f'RES<- InsertDocument:{res.request_id} {res.response_code}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.get_event_loop().run_until_complete(main())