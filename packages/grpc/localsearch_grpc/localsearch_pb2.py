# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: localsearch.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11localsearch.proto\x12\x0blocalsearch\"Y\n\x15InsertDocumentRequest\x12\x12\n\nrequest_id\x18\x01 \x01(\t\x12\x13\n\x0b\x64ocument_id\x18\x02 \x01(\t\x12\x17\n\x0f\x63ontents_base64\x18\x03 \x01(\t\"C\n\x16InsertDocumentResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\t\x12\x15\n\rresponse_code\x18\x02 \x01(\r\"=\n\x12GetDocumentRequest\x12\x12\n\nrequest_id\x18\x01 \x01(\t\x12\x13\n\x0b\x64ocument_id\x18\x02 \x01(\t\"Y\n\x13GetDocumentResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\t\x12\x15\n\rresponse_code\x18\x02 \x01(\r\x12\x17\n\x0f\x63ontents_base64\x18\x03 \x01(\t\"1\n\x0cQueryRequest\x12\x12\n\nrequest_id\x18\x01 \x01(\t\x12\r\n\x05query\x18\x02 \x01(\t\"o\n\rQueryResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\t\x12\x15\n\rresponse_code\x18\x02 \x01(\r\x12\x33\n\x0f\x64ocument_scores\x18\x03 \x03(\x0b\x32\x1a.localsearch.DocumentScore\"\"\n\x0cIndexRequest\x12\x12\n\nrequest_id\x18\x01 \x01(\t\":\n\rIndexResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\t\x12\x15\n\rresponse_code\x18\x02 \x01(\r\"3\n\rDocumentScore\x12\x13\n\x0b\x64ocument_id\x18\x01 \x01(\t\x12\r\n\x05score\x18\x02 \x01(\x02\x32\xc2\x02\n\x0bLocalsearch\x12[\n\x0eInsertDocument\x12\".localsearch.InsertDocumentRequest\x1a#.localsearch.InsertDocumentResponse\"\x00\x12R\n\x0bGetDocument\x12\x1f.localsearch.GetDocumentRequest\x1a .localsearch.GetDocumentResponse\"\x00\x12@\n\x05Index\x12\x19.localsearch.IndexRequest\x1a\x1a.localsearch.IndexResponse\"\x00\x12@\n\x05Query\x12\x19.localsearch.QueryRequest\x1a\x1a.localsearch.QueryResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'localsearch_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_INSERTDOCUMENTREQUEST']._serialized_start=34
  _globals['_INSERTDOCUMENTREQUEST']._serialized_end=123
  _globals['_INSERTDOCUMENTRESPONSE']._serialized_start=125
  _globals['_INSERTDOCUMENTRESPONSE']._serialized_end=192
  _globals['_GETDOCUMENTREQUEST']._serialized_start=194
  _globals['_GETDOCUMENTREQUEST']._serialized_end=255
  _globals['_GETDOCUMENTRESPONSE']._serialized_start=257
  _globals['_GETDOCUMENTRESPONSE']._serialized_end=346
  _globals['_QUERYREQUEST']._serialized_start=348
  _globals['_QUERYREQUEST']._serialized_end=397
  _globals['_QUERYRESPONSE']._serialized_start=399
  _globals['_QUERYRESPONSE']._serialized_end=510
  _globals['_INDEXREQUEST']._serialized_start=512
  _globals['_INDEXREQUEST']._serialized_end=546
  _globals['_INDEXRESPONSE']._serialized_start=548
  _globals['_INDEXRESPONSE']._serialized_end=606
  _globals['_DOCUMENTSCORE']._serialized_start=608
  _globals['_DOCUMENTSCORE']._serialized_end=659
  _globals['_LOCALSEARCH']._serialized_start=662
  _globals['_LOCALSEARCH']._serialized_end=984
# @@protoc_insertion_point(module_scope)
