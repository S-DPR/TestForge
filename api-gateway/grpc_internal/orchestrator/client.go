package orchestratorv1

import (
	"bff/internal/model"
	"context"
	"encoding/json"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"log"
)

type OrchestratorClient struct {
	client TestForgeServiceClient
}

type OrchestratorInterface interface {
	RunTestClient(reqDto *model.TestExecutorReqDTO, ctx context.Context) (TestForgeService_TestExecutorClient, error)
}

func NewOrchestratorGRPCClient(addr string, creds credentials.TransportCredentials) (*OrchestratorClient, error) {
	conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(creds))
	if err != nil {
		return nil, err
	}

	client := NewTestForgeServiceClient(conn)

	return &OrchestratorClient{
		client: client,
	}, nil
}

func (o *OrchestratorClient) RunTestClient(reqDto *model.TestExecutorReqDTO, ctx context.Context) (TestForgeService_TestExecutorClient, error) {
	formatJson, err := json.Marshal(reqDto.TestcaseFormat)
	if err != nil {
		// 에러 처리 제대로 안 하면 진짜 바보다
		return nil, fmt.Errorf("testcaseFormat JSON marshal 실패: %v", err)
	}
	log.Println("sending testcaseFormat json:", string(formatJson))

	req := &TestExecutorReq{
		TestcaseFormat: string(formatJson),
		Code1:          reqDto.Code1,
		Code2:          reqDto.Code2,
		Timelimit:      reqDto.TimeLimit,
		RepeatCount:    reqDto.RepeatCount,
	}

	return o.client.TestExecutor(ctx, req)
}
