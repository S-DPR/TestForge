package orchestratorv1

import (
	"bff/internal/model"
	"context"
	"encoding/json"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"time"
)

type OrchestratorClient struct {
	client TestForgeServiceClient
}

type OrchestratorInterface interface {
	RunTestClient(reqDto *model.TestExecutorReqDTO) (TestForgeService_TestExecutorClient, error)
}

func NewOrchestratorGRPCClient(addr string, creds credentials.TransportCredentials) (*OrchestratorClient, error) {
	conn, err := grpc.NewClient(addr, grpc.WithTransportCredentials(creds))
	if err != nil {
		return nil, err
	}

	client := NewTestForgeServiceClient(conn)

	return &OrchestratorClient{
		client: client,
	}, nil
}

//func NewOrchestratorGRPCClient() (*OrchestratorClient, error) {
//	conn, err := grpc.NewClient("orchestrator:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
//	if err != nil {
//		return nil, err
//	}
//	client := NewTestForgeServiceClient(conn)
//
//	return &OrchestratorClient{
//		client: client,
//	}, nil
//}

//var client TestForgeServiceClient
//var conn *grpc.ClientConn
//
//func InitGRPCClient() {
//	if client != nil {
//		return
//	}
//	var err error
//	conn, err = grpc.NewClient("orchestrator:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
//	if err != nil {
//		log.Fatalf("gRPC 연결 실패: %v", err)
//	}
//	client = NewTestForgeServiceClient(conn)
//}
//
//func CloseGRPCClient() {
//	if conn != nil {
//		conn.Close()
//	}
//}

func (o *OrchestratorClient) RunTestClient(reqDto *model.TestExecutorReqDTO) (TestForgeService_TestExecutorClient, error) {
	formatJson, err := json.Marshal(reqDto.TestcaseFormat)
	if err != nil {
		// 에러 처리 제대로 안 하면 진짜 바보다
		return nil, fmt.Errorf("testcaseFormat JSON marshal 실패: %v", err)
	}

	req := &TestExecutorReq{
		TestcaseFormat: string(formatJson),
		Code1:          reqDto.Code1,
		Code2:          reqDto.Code2,
		Timelimit:      reqDto.TimeLimit,
		RepeatCount:    reqDto.RepeatCount,
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*300)
	defer cancel()

	return o.client.TestExecutor(ctx, req)
	//if err != nil {
	//	log.Fatalf("TestExecutor 호출 실패: %v", err)
	//}
	//
	//for {
	//	res, err := stream.Recv()
	//	if err == io.EOF {
	//		log.Println("결과 스트리밍 끝")
	//		break
	//	}
	//	if err != nil {
	//		log.Fatalf("스트리밍 중 에러: %v", err)
	//	}
	//
	//	log.Printf("[결과] 파일: %s, 상태: %s", res.GetFilename(), res.GetDiffStatus())
	//	return res
	//}
}
