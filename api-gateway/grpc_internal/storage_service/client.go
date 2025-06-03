package storage_servicev1

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

type StorageServiceClient struct {
	client FileClient
}

type StorageServiceInterface interface {
	Read(filename string, ctx context.Context) (*FileReadRes, error)
}

func NewStorageServiceGRPCClient(addr string, creds credentials.TransportCredentials) (*StorageServiceClient, error) {
	conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(creds))
	if err != nil {
		return nil, err
	}

	client := NewFileClient(conn)

	return &StorageServiceClient{
		client: client,
	}, nil
}

func (o *StorageServiceClient) Read(filename string, ctx context.Context) (*FileReadRes, error) {
	req := &FileReadReq{
		Folder:   "/scripts",
		Filename: filename,
		Ext:      "in",
	}

	return o.client.FileRead(ctx, req)
}
