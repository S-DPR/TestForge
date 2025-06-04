package service

import (
	storage_servicev1 "bff/grpc_internal/storage_service"
	"context"
)

type StorageService struct {
	client storage_servicev1.StorageServiceInterface
}

type StorageServiceInterface interface {
	Read(filename string, ctx context.Context) (*storage_servicev1.FileReadRes, error)
}

func NewStorageService(client storage_servicev1.StorageServiceInterface) *StorageService {
	return &StorageService{client}
}

func (t *StorageService) Read(filename string, ctx context.Context) (*storage_servicev1.FileReadRes, error) {
	return t.client.Read(filename, ctx)
}
