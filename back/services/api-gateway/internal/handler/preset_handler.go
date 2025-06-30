package handler

import (
	preset_servicev1 "bff/grpc_internal/input_generator_service"
	"bff/internal/service"
	"github.com/gin-gonic/gin"
	"net/http"
	"time"
)

type PresetHandler struct {
	PresetHandlerService service.PresetServiceInterface
}

type PresetServiceInterface interface {
	CreatePreset(c *gin.Context, req *preset_servicev1.PresetCreateRequest)
	GetPreset(c *gin.Context, req *preset_servicev1.PresetIdRequest)
	GetAllPresets(c *gin.Context, req *preset_servicev1.PresetListRequest)
	UpdatePreset(c *gin.Context, req *preset_servicev1.PresetUpdateRequest)
	DeletePreset(c *gin.Context, req *preset_servicev1.PresetIdRequest)
}

func NewPresetHandler(service service.PresetServiceInterface) *PresetHandler {
	return &PresetHandler{service}
}

func (h *PresetHandler) CreatePreset(c *gin.Context, req *preset_servicev1.PresetCreateRequest) {
	res, err := h.PresetHandlerService.CreatePreset(c, req)
	if err != nil {
		c.Error(err)
		return
	}

	c.JSON(200, gin.H{
		"preset_id":   res.PresetID,
		"preset_name": res.PresetName,
		"preset_type": res.PresetType,
		"content":     res.Content,
		"account_id":  res.AccountID,
		"create_dt":   res.CreateDt.AsTime(),
		"update_dt":   res.UpdateDt.AsTime(),
	})
}

func (h *PresetHandler) GetPreset(c *gin.Context, req *preset_servicev1.PresetIdRequest) {
	res, err := h.PresetHandlerService.GetPreset(c, req)
	if err != nil {
		c.Error(err)
		return
	}
	c.JSON(200, gin.H{
		"preset_id":   res.PresetId,
		"preset_name": res.PresetName,
		"preset_type": res.PresetType,
		"content":     res.Content,
		"create_dt":   res.CreateDt.AsTime(),
		"update_dt":   res.UpdateDt.AsTime(),
	})
}

func (h *PresetHandler) GetAllPresets(c *gin.Context, req *preset_servicev1.PresetListRequest) {
	res, err := h.PresetHandlerService.GetAllPresets(c, req)
	if err != nil {
		c.Error(err)
		return
	}
	response := []gin.H{}
	for _, p := range res.Presets {
		response = append(response, gin.H{
			"preset_id":   p.PresetId,
			"preset_name": p.PresetName,
			"preset_type": p.PresetType,
			"content":     p.Content,
			"create_dt":   p.CreateDt.AsTime(),
			"update_dt":   p.UpdateDt.AsTime(),
		})
	}

	c.JSON(http.StatusOK, gin.H{
		"presets": response,
	})
}

func (h *PresetHandler) UpdatePreset(c *gin.Context, req *preset_servicev1.PresetUpdateRequest) {
	res, err := h.PresetHandlerService.UpdatePreset(c, req)
	if err != nil {
		c.Error(err)
		return
	}
	c.JSON(200, gin.H{
		"preset_id":   res.PresetId,
		"preset_name": res.PresetName,
		"preset_type": res.PresetType,
		"content":     res.Content,
		"create_dt":   res.CreateDt.AsTime(),
		"update_dt":   res.UpdateDt.AsTime(),
	})
}

func (h *PresetHandler) DeletePreset(c *gin.Context, req *preset_servicev1.PresetIdRequest) {
	res, err := h.PresetHandlerService.DeletePreset(c, req)
	if err != nil {
		c.Error(err)
		return
	}
	c.JSON(200, gin.H{
		"preset_id":   res.PresetId,
		"preset_name": res.PresetName,
		"preset_type": res.PresetType,
		"content":     res.Content,
		"create_dt":   res.CreateDt.AsTime(),
		"update_dt":   res.UpdateDt.AsTime(),
	})
}
