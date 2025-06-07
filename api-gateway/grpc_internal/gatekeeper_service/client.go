package gatekeeper_servicev1

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

type GatekeeperServiceClient struct {
	client GatekeeperClient
}

type GatekeeperInterface interface {
	ValidateJwt(ctx context.Context, accessToken string) (*ValidateJwtRes, error)
}

func NewGatekeeperGRPCClient(addr string, creds credentials.TransportCredentials) (*GatekeeperServiceClient, error) {
	conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(creds))
	if err != nil {
		return nil, err
	}

	client := NewGatekeeperClient(conn)

	return &GatekeeperServiceClient{
		client: client,
	}, nil
}

func (r *GatekeeperServiceClient) ValidateJwt(ctx context.Context, accessToken string) (*ValidateJwtRes, error) {
	req := &ValidateJwtReq{
		AccessToken: accessToken,
	}

	return r.client.ValidateJwt(ctx, req)
}
