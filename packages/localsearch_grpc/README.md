## localsearch-grpc

Generated Protobuf and GRPC libraries for the localsearch service


### Usage
From within this monorepo, you can install this package as an editable local installation. Shown using poetry below.

``` toml
# packages/my-package/pyproject.toml

[tool.poetry.dependencies]
localsearch_grpc = {path = "../localsearch_grpc", develop=true}
```

Once the package is installed, you can import it like this:
```python
import grpc

from localsearch_grpc import localsearch_pb2
from localsearch_grpc import localsearch_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = localsearch_pb2_grpc.LocalsearchStub(channel)
stub.InsertDocument(localsearch_pb2.InsertDocumentRequest(
    request_id = '',
    document_id = '',
    contents_base64 = ''
))
```


Specific usage for this library can be found in the server/ and e2e/ packages.

More general usage docs on geneated grpc code can be found here: https://grpc.io/docs/languages/python/basics/