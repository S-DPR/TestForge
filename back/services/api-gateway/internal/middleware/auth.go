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
		if !SetAccountId(c) {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing or invalid token"})
			return
		}
		c.Next()
	}
}

func SetAccountId(c *gin.Context) bool {
	token, err := c.Cookie("access_token")
	if err != nil || token == "" {
		return false
	}

	accountId, err := getGatekeeperService().ValidateJwt(token, context.Background())
	if err != nil {
		return false
	}

	c.Set("accountId", accountId)
	return true
}
