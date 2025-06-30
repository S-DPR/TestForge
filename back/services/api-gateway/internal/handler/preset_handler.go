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
		"create_dt":   res.CreateDt.Format(time.RFC3339),
		"update_dt":   res.UpdateDt.Format(time.RFC3339),
	})
}

func (h *PresetHandler) GetPreset(c *gin.Context, req *preset_servicev1.PresetIdRequest) {
	res, err := h.PresetHandlerService.GetPreset(c, req)
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
		"create_dt":   res.CreateDt.Format(time.RFC3339),
		"update_dt":   res.UpdateDt.Format(time.RFC3339),
	})
}

func (h *PresetHandler) GetAllPresets(c *gin.Context, req *preset_servicev1.PresetListRequest) {
	res, err := h.PresetHandlerService.GetAllPresets(c, req)
	if err != nil {
		c.Error(err)
		return
	}
	response := []gin.H{}
	for _, p := range res {
		response = append(response, gin.H{
			"preset_id":   p.PresetID,
			"preset_name": p.PresetName,
			"preset_type": p.PresetType,
			"content":     p.Content,
			"account_id":  p.AccountID,
			"create_dt":   p.CreateDt.Format(time.RFC3339),
			"update_dt":   p.UpdateDt.Format(time.RFC3339),
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
		"preset_id":   res.PresetID,
		"preset_name": res.PresetName,
		"preset_type": res.PresetType,
		"content":     res.Content,
		"account_id":  res.AccountID,
		"create_dt":   res.CreateDt.Format(time.RFC3339),
		"update_dt":   res.UpdateDt.Format(time.RFC3339),
	})
}

func (h *PresetHandler) DeletePreset(c *gin.Context, req *preset_servicev1.PresetIdRequest) {
	res, err := h.PresetHandlerService.DeletePreset(c, req)
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
		"create_dt":   res.CreateDt.Format(time.RFC3339),
		"update_dt":   res.UpdateDt.Format(time.RFC3339),
	})
}
