package rate_limit_servicev1

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

type RateLimitClient struct {
	client LimitClient
}

type RateLimitInterface interface {
	CheckExecutionLimit(ctx context.Context, accountID string, count int32) (*TestExecutionLimitRes, error)
}

func NewRateLimitGRPCClient(addr string, creds credentials.TransportCredentials) (*RateLimitClient, error) {
	conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(creds))
	if err != nil {
		return nil, err
	}

	client := NewLimitClient(conn)

	return &RateLimitClient{
		client: client,
	}, nil
}

func (r *RateLimitClient) CheckExecutionLimit(ctx context.Context, accountID string, count int32) (*TestExecutionLimitRes, error) {
	req := &TestExecutionLimitReq{
		AccountId: accountID,
		Count:     count,
	}

	return r.client.TestExecutionLimit(ctx, req)
}
