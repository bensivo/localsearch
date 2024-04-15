import asyncio
import logging

from localsearch_server.controller import GrpcController
from localsearch_server.tokenizer import Tokenizer
from localsearch_server.tf_index import FileTFIndex
from localsearch_server.document_store import FileDocumentStore


async def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'Downloading tokenization data')

    tokenizer = Tokenizer()
    tokenizer.init()

    document_store = FileDocumentStore(
        base_dir='./data/documents'
    )
    document_store.init()

    tf_index = FileTFIndex(
        filepath='./data/tf_index.json'
    )
    tf_index.init()

    controller = GrpcController(
        port = 50051,
        tokenizer = tokenizer,
        document_store = document_store,
        tf_index = tf_index
    )

    await controller.start()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())