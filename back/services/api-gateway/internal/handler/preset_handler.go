package handler

import (
	"bff/internal/model"
	"bff/internal/service"
	"github.com/gin-gonic/gin"
	"net/http"
	"time"
)

type PresetHandler struct {
	PresetHandlerService service.PresetServiceInterface
}

type PresetServiceInterface interface {
	CreatePreset(c *gin.Context, req *model.PresetCreateReqDTO)
	GetPreset(c *gin.Context, req *model.PresetIdReqDTO)
	GetAllPresets(c *gin.Context, req *model.PresetListReqDTO)
	UpdatePreset(c *gin.Context, req *model.PresetUpdateReqDTO)
	DeletePreset(c *gin.Context, req *model.PresetIdReqDTO)
}

func NewPresetHandler(service service.PresetServiceInterface) *PresetHandler {
	return &PresetHandler{service}
}

func (h *PresetHandler) CreatePreset(c *gin.Context, req *model.PresetCreateReqDTO) {
	accountIdAny, exist := c.Get("accountId")
	if !exist {
		c.JSON(401, gin.H{"error": "account id not found"})
	}
	accountId := accountIdAny.(string)

	res, err := h.PresetHandlerService.CreatePreset(c, req, accountId)
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

func (h *PresetHandler) GetPreset(c *gin.Context, req *model.PresetIdReqDTO) {
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

func (h *PresetHandler) GetAllPresets(c *gin.Context, req *model.PresetListReqDTO) {
	accountIdAny, exist := c.Get("accountId")
	if !exist {
		c.JSON(401, gin.H{"error": "account id not found"})
	}
	accountId := accountIdAny.(string)

	res, err := h.PresetHandlerService.GetAllPresets(c, req, accountId)
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

func (h *PresetHandler) UpdatePreset(c *gin.Context, req *model.PresetUpdateReqDTO) {
	accountIdAny, exist := c.Get("accountId")
	if !exist {
		c.JSON(401, gin.H{"error": "account id not found"})
	}
	accountId := accountIdAny.(string)

	res, err := h.PresetHandlerService.UpdatePreset(c, req, accountId)
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

func (h *PresetHandler) DeletePreset(c *gin.Context, req *model.PresetIdReqDTO) {
	accountIdAny, exist := c.Get("accountId")
	if !exist {
		c.JSON(401, gin.H{"error": "account id not found"})
	}
	accountId := accountIdAny.(string)

	_, err := h.PresetHandlerService.DeletePreset(c, req, accountId)
	if err != nil {
		c.Error(err)
		return
	}
	c.JSON(200, gin.H{})
}
