package router

import (
	orchestratorv1 "bff/grpc_internal/orchestrator"
	storage_servicev1 "bff/grpc_internal/storage_service"
	"bff/internal/handler"
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
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept"},
		AllowCredentials: true,
	}))

	grpcClient, _ := orchestratorv1.NewOrchestratorGRPCClient("orchestrator:50051", insecure.NewCredentials())
	executorService := service.NewTestExecutorService(grpcClient)
	executorHandler := handler.NewTestExecutorHandler(executorService)
	r.POST("/test-execute", func(c *gin.Context) {
		var req model.TestExecutorReqDTO
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		executorHandler.TestExecute(c, &req)
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
