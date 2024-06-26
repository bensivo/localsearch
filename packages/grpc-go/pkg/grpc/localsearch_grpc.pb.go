// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             v3.20.3
// source: localsearch.proto

package grpc

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// LocalsearchClient is the client API for Localsearch service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type LocalsearchClient interface {
	InsertDocument(ctx context.Context, in *InsertDocumentRequest, opts ...grpc.CallOption) (*InsertDocumentResponse, error)
	GetDocument(ctx context.Context, in *GetDocumentRequest, opts ...grpc.CallOption) (*GetDocumentResponse, error)
	ListDocuments(ctx context.Context, in *ListDocumentsRequest, opts ...grpc.CallOption) (*ListDocumentsResponse, error)
	Index(ctx context.Context, in *IndexRequest, opts ...grpc.CallOption) (*IndexResponse, error)
	Query(ctx context.Context, in *QueryRequest, opts ...grpc.CallOption) (*QueryResponse, error)
}

type localsearchClient struct {
	cc grpc.ClientConnInterface
}

func NewLocalsearchClient(cc grpc.ClientConnInterface) LocalsearchClient {
	return &localsearchClient{cc}
}

func (c *localsearchClient) InsertDocument(ctx context.Context, in *InsertDocumentRequest, opts ...grpc.CallOption) (*InsertDocumentResponse, error) {
	out := new(InsertDocumentResponse)
	err := c.cc.Invoke(ctx, "/localsearch.Localsearch/InsertDocument", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *localsearchClient) GetDocument(ctx context.Context, in *GetDocumentRequest, opts ...grpc.CallOption) (*GetDocumentResponse, error) {
	out := new(GetDocumentResponse)
	err := c.cc.Invoke(ctx, "/localsearch.Localsearch/GetDocument", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *localsearchClient) ListDocuments(ctx context.Context, in *ListDocumentsRequest, opts ...grpc.CallOption) (*ListDocumentsResponse, error) {
	out := new(ListDocumentsResponse)
	err := c.cc.Invoke(ctx, "/localsearch.Localsearch/ListDocuments", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *localsearchClient) Index(ctx context.Context, in *IndexRequest, opts ...grpc.CallOption) (*IndexResponse, error) {
	out := new(IndexResponse)
	err := c.cc.Invoke(ctx, "/localsearch.Localsearch/Index", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *localsearchClient) Query(ctx context.Context, in *QueryRequest, opts ...grpc.CallOption) (*QueryResponse, error) {
	out := new(QueryResponse)
	err := c.cc.Invoke(ctx, "/localsearch.Localsearch/Query", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// LocalsearchServer is the server API for Localsearch service.
// All implementations must embed UnimplementedLocalsearchServer
// for forward compatibility
type LocalsearchServer interface {
	InsertDocument(context.Context, *InsertDocumentRequest) (*InsertDocumentResponse, error)
	GetDocument(context.Context, *GetDocumentRequest) (*GetDocumentResponse, error)
	ListDocuments(context.Context, *ListDocumentsRequest) (*ListDocumentsResponse, error)
	Index(context.Context, *IndexRequest) (*IndexResponse, error)
	Query(context.Context, *QueryRequest) (*QueryResponse, error)
	mustEmbedUnimplementedLocalsearchServer()
}

// UnimplementedLocalsearchServer must be embedded to have forward compatible implementations.
type UnimplementedLocalsearchServer struct {
}

func (UnimplementedLocalsearchServer) InsertDocument(context.Context, *InsertDocumentRequest) (*InsertDocumentResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method InsertDocument not implemented")
}
func (UnimplementedLocalsearchServer) GetDocument(context.Context, *GetDocumentRequest) (*GetDocumentResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetDocument not implemented")
}
func (UnimplementedLocalsearchServer) ListDocuments(context.Context, *ListDocumentsRequest) (*ListDocumentsResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method ListDocuments not implemented")
}
func (UnimplementedLocalsearchServer) Index(context.Context, *IndexRequest) (*IndexResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Index not implemented")
}
func (UnimplementedLocalsearchServer) Query(context.Context, *QueryRequest) (*QueryResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Query not implemented")
}
func (UnimplementedLocalsearchServer) mustEmbedUnimplementedLocalsearchServer() {}

// UnsafeLocalsearchServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to LocalsearchServer will
// result in compilation errors.
type UnsafeLocalsearchServer interface {
	mustEmbedUnimplementedLocalsearchServer()
}

func RegisterLocalsearchServer(s grpc.ServiceRegistrar, srv LocalsearchServer) {
	s.RegisterService(&Localsearch_ServiceDesc, srv)
}

func _Localsearch_InsertDocument_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(InsertDocumentRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(LocalsearchServer).InsertDocument(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/localsearch.Localsearch/InsertDocument",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(LocalsearchServer).InsertDocument(ctx, req.(*InsertDocumentRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Localsearch_GetDocument_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetDocumentRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(LocalsearchServer).GetDocument(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/localsearch.Localsearch/GetDocument",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(LocalsearchServer).GetDocument(ctx, req.(*GetDocumentRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Localsearch_ListDocuments_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ListDocumentsRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(LocalsearchServer).ListDocuments(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/localsearch.Localsearch/ListDocuments",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(LocalsearchServer).ListDocuments(ctx, req.(*ListDocumentsRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Localsearch_Index_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(IndexRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(LocalsearchServer).Index(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/localsearch.Localsearch/Index",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(LocalsearchServer).Index(ctx, req.(*IndexRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Localsearch_Query_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(QueryRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(LocalsearchServer).Query(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/localsearch.Localsearch/Query",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(LocalsearchServer).Query(ctx, req.(*QueryRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// Localsearch_ServiceDesc is the grpc.ServiceDesc for Localsearch service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Localsearch_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "localsearch.Localsearch",
	HandlerType: (*LocalsearchServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "InsertDocument",
			Handler:    _Localsearch_InsertDocument_Handler,
		},
		{
			MethodName: "GetDocument",
			Handler:    _Localsearch_GetDocument_Handler,
		},
		{
			MethodName: "ListDocuments",
			Handler:    _Localsearch_ListDocuments_Handler,
		},
		{
			MethodName: "Index",
			Handler:    _Localsearch_Index_Handler,
		},
		{
			MethodName: "Query",
			Handler:    _Localsearch_Query_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "localsearch.proto",
}
