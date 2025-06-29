package input_generator_servicev1

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

type PresetServiceClient struct {
	client PresetClient
}

type PresetServiceInterface interface {
	CreatePreset(ctx context.Context, req *PresetCreateRequest) (*PresetResponse, error)
	GetPreset(ctx context.Context, req *PresetIdRequest) (*PresetResponse, error)
	GetAllPresets(ctx context.Context, req *PresetListRequest) (*PresetListResponse, error)
	UpdatePreset(ctx context.Context, req *PresetUpdateRequest) (*PresetResponse, error)
	DeletePreset(ctx context.Context, req *PresetIdRequest) (*DeletePresetResponse, error)
}

func NewInputGenGRPCClient(addr string, creds credentials.TransportCredentials) (*PresetServiceClient, error) {
	conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(creds))
	if err != nil {
		return nil, err
	}

	client := NewPresetClient(conn)

	return &PresetServiceClient{
		client: client,
	}, nil
}

func (c *PresetServiceClient) CreatePreset(ctx context.Context, req *PresetCreateRequest) (*PresetResponse, error) {
	return c.client.CreatePreset(ctx, req)
}

func (c *PresetServiceClient) GetPreset(ctx context.Context, req *PresetIdRequest) (*PresetResponse, error) {
	return c.client.GetPreset(ctx, req)
}

func (c *PresetServiceClient) GetAllPresets(ctx context.Context, req *PresetListRequest) (*PresetListResponse, error) {
	return c.client.GetAllPresets(ctx, req)
}

func (c *PresetServiceClient) UpdatePreset(ctx context.Context, req *PresetUpdateRequest) (*PresetResponse, error) {
	return c.client.UpdatePreset(ctx, req)
}

func (c *PresetServiceClient) DeletePreset(ctx context.Context, req *PresetIdRequest) (*DeletePresetResponse, error) {
	return c.client.DeletePreset(ctx, req)
}
