package router

import (
	input_generator_servicev1 "bff/grpc_internal/input_generator_service"
	orchestratorv1 "bff/grpc_internal/orchestrator"
	rate_limit_servicev1 "bff/grpc_internal/rate_limit_service"
	storage_servicev1 "bff/grpc_internal/storage_service"
	"bff/internal/handler"
	"bff/internal/middleware"
	"bff/internal/model"
	"bff/internal/service"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc/credentials/insecure"
	"net/http"
)

func New() *gin.Engine {
	r := gin.Default()

	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000"},
		AllowMethods:     []string{"GET", "POST", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept", "Authorization"},
		AllowCredentials: true,
	}))
	r.Use(middleware.AuthMiddleware())

	presetGrpcClient, _ := input_generator_servicev1.NewInputGenGRPCClient("input-generator-service:50051", insecure.NewCredentials())
	presetService := service.NewPresetService(presetGrpcClient)
	presetHandler := handler.NewPresetHandler(presetService)
	preset := r.Group("/preset")
	preset.POST("", func(c *gin.Context) {
		var req input_generator_servicev1.PresetCreateRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		presetHandler.CreatePreset(c, &req)
	})
	preset.PUT("", func(c *gin.Context) {
		var req input_generator_servicev1.PresetUpdateRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		presetHandler.UpdatePreset(c, &req)
	})
	preset.DELETE("/:presetId", func(c *gin.Context) {
		presetId := c.Param("presetId")
		presetHandler.DeletePreset(c, &input_generator_servicev1.PresetIdRequest{PresetId: presetId})
	})
	preset.GET("/:presetId", func(c *gin.Context) {
		presetId := c.Param("presetId")
		presetHandler.GetPreset(c, &input_generator_servicev1.PresetIdRequest{PresetId: presetId})
	})
	preset.POST("/search", func(c *gin.Context) {
		var req input_generator_servicev1.PresetListRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		presetHandler.GetAllPresets(c, &req)
	})

	rateLimitRrpcClient, _ := rate_limit_servicev1.NewRateLimitGRPCClient("rate-limit-service:50051", insecure.NewCredentials())
	rateLimitService := service.NewRateLimitService(rateLimitRrpcClient)

	grpcClient, _ := orchestratorv1.NewOrchestratorGRPCClient("orchestrator:50051", insecure.NewCredentials())
	executorService := service.NewTestExecutorService(grpcClient)
	executorHandler := handler.NewTestExecutorHandler(executorService)
	r.POST("/test-execute", func(c *gin.Context) {
		var req model.TestExecutorReqDTO
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		executorHandler.TestExecute(c, *rateLimitService, &req)
	})

	storageRrpcClient, _ := storage_servicev1.NewStorageServiceGRPCClient("storage-service:50051", insecure.NewCredentials())
	storageService := service.NewStorageService(storageRrpcClient)
	storageHandler := handler.NewStorageHandler(storageService)
	r.GET("/file/:filename", func(c *gin.Context) {
		filename := c.Param("filename")
		storageHandler.Read(c, filename)
	})

	//v1 := r.Group("v1")
	//{
	//	v1.GET("/hello", handler.GetV1)
	//}

	return r
}
