import asyncio
import logging

from localsearch_server.tf_index import InMemoryTFIndex
from localsearch_server.tf_inverted_index import InMemoryTFInvertedIndex
from localsearch_server.document_store import InMemoryDocumentStore
from localsearch_server.tokenizer import NaiveTokenizer
from localsearch_server.bm25 import BM25
from localsearch_server.service import LocalsearchService


async def main():
    logging.basicConfig(level=logging.DEBUG)

    tokenizer = NaiveTokenizer()
    tf_index = InMemoryTFIndex()
    tf_inverted_index = InMemoryTFInvertedIndex()
    document_store = InMemoryDocumentStore()
    bm25 = BM25(tf_index, tf_inverted_index, document_store)

    service = LocalsearchService(
        tokenizer=tokenizer,
        tf_index=tf_index,
        tf_inverted_index=tf_inverted_index,
        document_store=document_store,
        bm25=bm25,
    )

    service.insert_document(1, "Hello world")
    service.insert_document(2, "Goodbye, cruel world")
    service.insert_document(3, "The world says")

    print('"hello": ', service.query('hello'))
    print('"goodbye": ', service.query('goodbye'))
    print('"says": ', service.query('says'))

    # controller = GrpcController(
    #     port = 50051,
    #     tokenizer = tokenizer,
    #     document_store = document_store,
    #     tf_index = tf_index
    # )

    # await controller.start()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())