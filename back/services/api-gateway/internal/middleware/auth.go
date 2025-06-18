package middleware

import (
	gatekeeper_servicev1 "bff/grpc_internal/gatekeeper_service"
	"bff/internal/service"
	"context"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc/credentials/insecure"
	"net/http"
)

var gatekeeperService *service.GatekeeperService

func getGatekeeperService() *service.GatekeeperService {
	if gatekeeperService == nil {
		client, err := gatekeeper_servicev1.NewGatekeeperGRPCClient("gatekeeper-service:50051", insecure.NewCredentials())
		if err != nil {
			panic(err)
		}
		gatekeeperService = service.NewGatekeeperService(client)
	}
	return gatekeeperService
}

func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		token, err := c.Cookie("access_token")
		if err != nil || token == "" {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing or invalid token"})
			return
		}

		accountId, err := getGatekeeperService().ValidateJwt(token, context.Background())
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
			return
		}

		c.Set("accountId", accountId)
		c.Next()
	}
}
