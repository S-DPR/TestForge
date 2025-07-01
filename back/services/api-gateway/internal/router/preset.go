package router

import (
	input_generator_service "bff/grpc_internal/input_generator_service"
	"bff/internal/handler"
	"bff/internal/middleware"
	"bff/internal/model"
	"bff/internal/service"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc/credentials/insecure"
	"net/http"
)

func RegisterPresetRoutes(r *gin.Engine) {
	presetGrpcClient, _ := input_generator_service.NewInputGenGRPCClient("input-generator-service:50051", insecure.NewCredentials())
	presetService := service.NewPresetService(presetGrpcClient)
	presetHandler := handler.NewPresetHandler(presetService)

	publicPresetRoutes(r, presetHandler)
	privatePresetRoutes(r, presetHandler)
}

func publicPresetRoutes(r *gin.Engine, presetHandler *handler.PresetHandler) {
	preset := r.Group("/preset")
	{
		preset.GET("/:presetId", func(c *gin.Context) {
			presetId := c.Param("presetId")
			presetHandler.GetPreset(c, &model.PresetIdReqDTO{PresetId: presetId})
		})

		preset.POST("/search", func(c *gin.Context) {
			var req model.PresetListReqDTO
			if err := c.ShouldBindJSON(&req); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			presetHandler.GetAllPresets(c, &req)
		})
	}
}

func privatePresetRoutes(r *gin.Engine, presetHandler *handler.PresetHandler) {
	preset := r.Group("/preset", middleware.AuthMiddleware())
	{
		preset.POST("", func(c *gin.Context) {
			var req model.PresetCreateReqDTO
			if err := c.ShouldBindJSON(&req); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			presetHandler.CreatePreset(c, &req)
		})

		preset.PUT("", func(c *gin.Context) {
			var req model.PresetUpdateReqDTO
			if err := c.ShouldBindJSON(&req); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			presetHandler.UpdatePreset(c, &req)
		})

		preset.DELETE("/:presetId", func(c *gin.Context) {
			presetId := c.Param("presetId")
			presetHandler.DeletePreset(c, &model.PresetIdReqDTO{PresetId: presetId})
		})
	}
}
