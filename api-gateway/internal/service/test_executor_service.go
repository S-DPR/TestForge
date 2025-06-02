package service

import (
	orchestratorv1 "bff/grpc_internal/orchestrator"
	"bff/internal/model"
	"context"
)

type TestExecutorService struct {
	client orchestratorv1.OrchestratorInterface
}

type TestExecutorServiceInterface interface {
	TestExecute(req *model.TestExecutorReqDTO, ctx context.Context) (orchestratorv1.TestForgeService_TestExecutorClient, error)
}

func NewTestExecutorService(client orchestratorv1.OrchestratorInterface) *TestExecutorService {
	return &TestExecutorService{client}
}

func (t *TestExecutorService) TestExecute(req *model.TestExecutorReqDTO, ctx context.Context) (orchestratorv1.TestForgeService_TestExecutorClient, error) {
	stream, err := t.client.RunTestClient(req, ctx)
	if err != nil {
		return nil, err
	}
	return stream, err
}
