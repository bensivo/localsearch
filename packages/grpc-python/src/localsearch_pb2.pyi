from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

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
