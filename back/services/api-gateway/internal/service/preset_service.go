package service

import (
	preset_servicev1 "bff/grpc_internal/input_generator_service"
	"context"
)

type PresetService struct {
	client preset_servicev1.PresetServiceInterface
}

type PresetServiceInterface interface {
	CreatePreset(ctx context.Context, req *preset_servicev1.PresetCreateRequest) (*preset_servicev1.PresetResponse, error)
	GetPreset(ctx context.Context, req *preset_servicev1.PresetIdRequest) (*preset_servicev1.PresetResponse, error)
	GetAllPresets(ctx context.Context, req *preset_servicev1.PresetListRequest) (*preset_servicev1.PresetListResponse, error)
	UpdatePreset(ctx context.Context, req *preset_servicev1.PresetUpdateRequest) (*preset_servicev1.PresetResponse, error)
	DeletePreset(ctx context.Context, req *preset_servicev1.PresetIdRequest) (*preset_servicev1.DeletePresetResponse, error)
}

func NewPresetService(client preset_servicev1.PresetServiceInterface) *PresetService {
	return &PresetService{client}
}

func (c *PresetService) CreatePreset(ctx context.Context, req *preset_servicev1.PresetCreateRequest) (*preset_servicev1.PresetResponse, error) {
	return c.client.CreatePreset(ctx, req)
}

func (c *PresetService) GetPreset(ctx context.Context, req *preset_servicev1.PresetIdRequest) (*preset_servicev1.PresetResponse, error) {
	return c.client.GetPreset(ctx, req)
}

func (c *PresetService) GetAllPresets(ctx context.Context, req *preset_servicev1.PresetListRequest) (*preset_servicev1.PresetListResponse, error) {
	return c.client.GetAllPresets(ctx, req)
}

func (c *PresetService) UpdatePreset(ctx context.Context, req *preset_servicev1.PresetUpdateRequest) (*preset_servicev1.PresetResponse, error) {
	return c.client.UpdatePreset(ctx, req)
}

func (c *PresetService) DeletePreset(ctx context.Context, req *preset_servicev1.PresetIdRequest) (*preset_servicev1.DeletePresetResponse, error) {
	return c.client.DeletePreset(ctx, req)
}
