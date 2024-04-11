import asyncio
import logging

from controller import GrpcController
from tokenization import Tokenizer
from document_store import FileDocumentStore


async def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'Downloading tokenization data')

    tokenizer = Tokenizer()
    tokenizer.init()

    document_store = FileDocumentStore(
        base_dir='./data/documents'
    )
    document_store.init()

    controller = GrpcController(
        port = 50051,
        tokenizer = tokenizer,
        document_store = document_store,
    )
    await controller.start()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())