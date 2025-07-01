package router

import (
	orchestrator "bff/grpc_internal/orchestrator"
	rate_limit_service "bff/grpc_internal/rate_limit_service"
	"bff/internal/handler"
	"bff/internal/middleware"
	"bff/internal/model"
	"bff/internal/service"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc/credentials/insecure"
	"net/http"
)

func RegisterExecutorRoutes(r *gin.Engine) {
	grpcClient, _ := orchestrator.NewOrchestratorGRPCClient("orchestrator:50051", insecure.NewCredentials())
	rateLimitClient, _ := rate_limit_service.NewRateLimitGRPCClient("rate-limit-service:50051", insecure.NewCredentials())

	executorService := service.NewTestExecutorService(grpcClient)
	rateLimitService := service.NewRateLimitService(rateLimitClient)
	executorHandler := handler.NewTestExecutorHandler(executorService)

	exec := r.Group("/test-execute", middleware.AuthMiddleware())
	{
		exec.POST("/test-execute", func(c *gin.Context) {
			var req model.TestExecutorReqDTO
			if err := c.ShouldBindJSON(&req); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			executorHandler.TestExecute(c, *rateLimitService, &req)
		})
	}
}
