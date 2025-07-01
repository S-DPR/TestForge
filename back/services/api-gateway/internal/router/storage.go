package router

import (
	storage_service "bff/grpc_internal/storage_service"
	"bff/internal/handler"
	"bff/internal/service"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc/credentials/insecure"
)

func RegisterStorageRoutes(r *gin.Engine) {
	storageClient, _ := storage_service.NewStorageServiceGRPCClient("storage-service:50051", insecure.NewCredentials())
	storageService := service.NewStorageService(storageClient)
	storageHandler := handler.NewStorageHandler(storageService)

	file := r.Group("file")
	{
		file.GET("/file/:filename", func(c *gin.Context) {
			filename := c.Param("filename")
			storageHandler.Read(c, filename)
		})
	}
}
