package service

import (
	gatekeeperServicev1 "bff/grpc_internal/gatekeeper_service"
	"context"
)

type GatekeeperService struct {
	client gatekeeperServicev1.GatekeeperInterface
}

type GatekeeperInterface interface {
	ValidateJwt(filename string, ctx context.Context) (*gatekeeperServicev1.ValidateJwtRes, error)
}

func NewGatekeeperService(client gatekeeperServicev1.GatekeeperInterface) *GatekeeperService {
	return &GatekeeperService{client}
}

func (g *GatekeeperService) ValidateJwt(token string, ctx context.Context) (string, error) {
	res, err := g.client.ValidateJwt(ctx, token)
	if err != nil {
		return "", err
	}
	return res.AccountId, nil
}
