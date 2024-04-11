# localsearch
A project on information retrieval, implementing text-document indexing and search using NLP and BM25


Implemented as a GRPC server and client. The server exposes core user-facing functions:
- InsertDocument() - Add a document to persistent storage
- GetDocument() - Fetch a document from persistent storage
- TODO: ListDocuments() - List documents that are available in persistent storage
- TODO: Index() - Re-build document index, indexing all documents in persistent storage
- TODO: Query() - Given a text query, returns the top N documents, based on the BM25 ranking algorithm


## References
References and tutorials I used when buildling this application:
- GRPC server, client setup: https://grpc.io/docs/languages/python/basics/
- Local package installations in python monorepos: https://pip.pypa.io/en/stable/topics/local-project-installs/
- Fake data generation for tesitng: https://github.com/joke2k/faker?tab=readme-ov-file

