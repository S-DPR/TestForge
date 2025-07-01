package service

import (
	preset_servicev1 "bff/grpc_internal/input_generator_service"
	"bff/internal/model"
	"context"
)

type PresetService struct {
	client preset_servicev1.PresetServiceInterface
}

type PresetServiceInterface interface {
	CreatePreset(ctx context.Context, req *model.PresetCreateReqDTO, accountId string) (*preset_servicev1.PresetResponse, error)
	GetPreset(ctx context.Context, req *model.PresetIdReqDTO) (*preset_servicev1.PresetResponse, error)
	GetAllPresets(ctx context.Context, req *model.PresetListReqDTO, accountId string) (*preset_servicev1.PresetListResponse, error)
	UpdatePreset(ctx context.Context, req *model.PresetUpdateReqDTO, accountId string) (*preset_servicev1.PresetResponse, error)
	DeletePreset(ctx context.Context, req *model.PresetIdReqDTO, accountId string) (*preset_servicev1.DeletePresetResponse, error)
}

func NewPresetService(client preset_servicev1.PresetServiceInterface) *PresetService {
	return &PresetService{client}
}

func (c *PresetService) CreatePreset(ctx context.Context, req *model.PresetCreateReqDTO, accountId string) (*preset_servicev1.PresetResponse, error) {
	request := preset_servicev1.PresetCreateRequest{
		PresetName: req.PresetName,
		PresetType: req.PresetType,
		Content:    req.Content,
		AccountId:  accountId,
	}
	return c.client.CreatePreset(ctx, &request)
}

func (c *PresetService) GetPreset(ctx context.Context, req *model.PresetIdReqDTO) (*preset_servicev1.PresetResponse, error) {
	request := preset_servicev1.PresetIdRequest{
		PresetId: req.PresetId,
	}
	return c.client.GetPreset(ctx, &request)
}

func (c *PresetService) GetAllPresets(ctx context.Context, req *model.PresetListReqDTO, accountId string) (*preset_servicev1.PresetListResponse, error) {
	request := preset_servicev1.PresetListRequest{
		AccountId: accountId,
		Page:      req.Page,
		Size:      req.Size,
	}
	return c.client.GetAllPresets(ctx, &request)
}

func (c *PresetService) UpdatePreset(ctx context.Context, req *model.PresetUpdateReqDTO, accountId string) (*preset_servicev1.PresetResponse, error) {
	request := preset_servicev1.PresetUpdateRequest{
		PresetId:   req.PresetId,
		PresetName: req.PresetName,
		PresetType: req.PresetType,
		Content:    req.Content,
		AccountId:  accountId,
	}
	return c.client.UpdatePreset(ctx, &request)
}

func (c *PresetService) DeletePreset(ctx context.Context, req *model.PresetIdReqDTO, accountId string) (*preset_servicev1.DeletePresetResponse, error) {
	request := preset_servicev1.PresetIdRequest{
		PresetId: req.PresetId,
	}
	return c.client.DeletePreset(ctx, &request)
}
