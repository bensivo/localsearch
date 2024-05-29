from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InsertDocumentRequest(_message.Message):
    __slots__ = ("request_id", "document_id", "contents_base64")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_BASE64_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    document_id: str
    contents_base64: str
    def __init__(self, request_id: _Optional[str] = ..., document_id: _Optional[str] = ..., contents_base64: _Optional[str] = ...) -> None: ...

class InsertDocumentResponse(_message.Message):
    __slots__ = ("request_id", "response_code")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_CODE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    response_code: int
    def __init__(self, request_id: _Optional[str] = ..., response_code: _Optional[int] = ...) -> None: ...

class GetDocumentRequest(_message.Message):
    __slots__ = ("request_id", "document_id")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    document_id: str
    def __init__(self, request_id: _Optional[str] = ..., document_id: _Optional[str] = ...) -> None: ...

class GetDocumentResponse(_message.Message):
    __slots__ = ("request_id", "response_code", "contents_base64")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_CODE_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_BASE64_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    response_code: int
    contents_base64: str
    def __init__(self, request_id: _Optional[str] = ..., response_code: _Optional[int] = ..., contents_base64: _Optional[str] = ...) -> None: ...

class ListDocumentsRequest(_message.Message):
    __slots__ = ("request_id", "limit", "offset")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    limit: int
    offset: int
    def __init__(self, request_id: _Optional[str] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class ListDocumentsResponse(_message.Message):
    __slots__ = ("request_id", "response_code", "documents")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_CODE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    response_code: int
    documents: _containers.RepeatedCompositeFieldContainer[DocumentMetadata]
    def __init__(self, request_id: _Optional[str] = ..., response_code: _Optional[int] = ..., documents: _Optional[_Iterable[_Union[DocumentMetadata, _Mapping]]] = ...) -> None: ...

class DocumentMetadata(_message.Message):
    __slots__ = ("document_id",)
    DOCUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    document_id: str
    def __init__(self, document_id: _Optional[str] = ...) -> None: ...

class QueryRequest(_message.Message):
    __slots__ = ("request_id", "query")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    query: str
    def __init__(self, request_id: _Optional[str] = ..., query: _Optional[str] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("request_id", "response_code", "document_scores")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_CODE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_SCORES_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    response_code: int
    document_scores: _containers.RepeatedCompositeFieldContainer[DocumentScore]
    def __init__(self, request_id: _Optional[str] = ..., response_code: _Optional[int] = ..., document_scores: _Optional[_Iterable[_Union[DocumentScore, _Mapping]]] = ...) -> None: ...

class IndexRequest(_message.Message):
    __slots__ = ("request_id",)
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    def __init__(self, request_id: _Optional[str] = ...) -> None: ...

class IndexResponse(_message.Message):
    __slots__ = ("request_id", "response_code")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_CODE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    response_code: int
    def __init__(self, request_id: _Optional[str] = ..., response_code: _Optional[int] = ...) -> None: ...

class DocumentScore(_message.Message):
    __slots__ = ("document_id", "score")
    DOCUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    document_id: str
    score: float
    def __init__(self, document_id: _Optional[str] = ..., score: _Optional[float] = ...) -> None: ...
