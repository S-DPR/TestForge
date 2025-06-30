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
		"presetId":   res.PresetId,
		"presetName": res.PresetName,
		"presetType": res.PresetType,
		"content":    res.Content,
		"createDt":   res.CreateDt.AsTime().Format(time.RFC3339),
		"updateDt":   res.UpdateDt.AsTime().Format(time.RFC3339),
	})
}

func (h *PresetHandler) GetPreset(c *gin.Context, req *preset_servicev1.PresetIdRequest) {
	res, err := h.PresetHandlerService.GetPreset(c, req)
	if err != nil {
		c.Error(err)
		return
	}
	c.JSON(200, gin.H{
		"presetId":   res.PresetId,
		"presetName": res.PresetName,
		"presetType": res.PresetType,
		"content":    res.Content,
		"createDt":   res.CreateDt.AsTime().Format(time.RFC3339),
		"updateDt":   res.UpdateDt.AsTime().Format(time.RFC3339),
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
			"presetId":   p.PresetId,
			"presetName": p.PresetName,
			"presetType": p.PresetType,
			"content":    p.Content,
			"createDt":   p.CreateDt.AsTime().Format(time.RFC3339),
			"updateDt":   p.UpdateDt.AsTime().Format(time.RFC3339),
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
		"presetId":   res.PresetId,
		"presetName": res.PresetName,
		"presetType": res.PresetType,
		"content":    res.Content,
		"createDt":   res.CreateDt.AsTime().Format(time.RFC3339),
		"updateDt":   res.UpdateDt.AsTime().Format(time.RFC3339),
	})
}

func (h *PresetHandler) DeletePreset(c *gin.Context, req *preset_servicev1.PresetIdRequest) {
	_, err := h.PresetHandlerService.DeletePreset(c, req)
	if err != nil {
		c.Error(err)
		return
	}
	c.JSON(200, gin.H{})
}
