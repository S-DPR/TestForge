package service

import (
	"context"

	ratelimitv1 "bff/grpc_internal/rate_limit_service"
)

type RateLimitService struct {
	client ratelimitv1.RateLimitInterface
}

type RateLimitServiceInterface interface {
	Check(accountID string, count int32, ctx context.Context) (*ratelimitv1.TestExecutionLimitRes, error)
}

func NewRateLimitService(client ratelimitv1.RateLimitInterface) *RateLimitService {
	return &RateLimitService{client}
}

func (r *RateLimitService) Check(accountID string, count int32, ctx context.Context) (*ratelimitv1.TestExecutionLimitRes, error) {
	return r.client.CheckExecutionLimit(ctx, accountID, count)
}
