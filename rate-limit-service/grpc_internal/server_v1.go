package grpc_internal

import (
	"context"
	"github.com/redis/go-redis/v9"
	"rate-limit-service/internal/service"
)

func serve() {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "",
		DB:       0,
	})
	client := service.NewTestExecutionLimitService(ctx, rdb)
}
