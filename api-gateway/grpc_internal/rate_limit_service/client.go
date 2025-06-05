package rate_limit_servicev1

import (
	"bff/grpc_internal/rate_limit_service"
	"context"
	"google.golang.org/grpc"
)

type RateLimitClient struct {
	client rate_limit_service.LimitClient
}

type RateLimitInterface interface {
	CheckExecutionLimit(ctx context.Context, accountID string, count int32) (*rate_limit_service.TestExecutionLimitRes, error)
}

func NewRateLimitGRPCClient(addr string, dialOpts ...grpc.DialOption) (*RateLimitClient, error) {
	conn, err := grpc.Dial(addr, dialOpts...)
	if err != nil {
		return nil, err
	}

	client := rate_limit_service.NewLimitClient(conn)

	return &RateLimitClient{
		client: client,
	}, nil
}

func (r *RateLimitClient) CheckExecutionLimit(ctx context.Context, accountID string, count int32) (*rate_limit_service.TestExecutionLimitRes, error) {
	req := &rate_limit_service.TestExecutionLimitReq{
		AccountId: accountID,
		Count:     count,
	}

	return r.client.TestExecutionLimit(ctx, req)
}
