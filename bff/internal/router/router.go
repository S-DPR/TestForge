package router

import (
	orchestratorv1 "bff/grpc_internal/orchestrator"
	"bff/internal/handler"
	"bff/internal/model"
	"bff/internal/service"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc/credentials/insecure"
	"net/http"
)

func New() *gin.Engine {
	r := gin.Default()

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

	//v1 := r.Group("v1")
	//{
	//	v1.GET("/hello", handler.GetV1)
	//}

	return r
}
