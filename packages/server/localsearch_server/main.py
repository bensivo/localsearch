import asyncio
import logging

from localsearch_server.tf_index import InMemoryTFIndex
from localsearch_server.tf_inverted_index import InMemoryTFInvertedIndex
from localsearch_server.document_store import InMemoryDocumentStore
from localsearch_server.tokenizer import NaiveTokenizer, NltkTokenizer
from localsearch_server.bm25 import BM25
from localsearch_server.service import LocalsearchService
from localsearch_server.controller import GrpcController


async def main():
    logging.basicConfig(level=logging.DEBUG)

    tokenizer = NltkTokenizer()
    tf_index = InMemoryTFIndex()
    tf_inverted_index = InMemoryTFInvertedIndex()
    document_store = InMemoryDocumentStore()

    tokenizer.init()

    service = LocalsearchService(
        tokenizer=tokenizer,
        tf_index=tf_index,
        tf_inverted_index=tf_inverted_index,
        document_store=document_store,
    )

    controller = GrpcController(
        port = 50051,
        service = service,
    )

    await controller.start()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())