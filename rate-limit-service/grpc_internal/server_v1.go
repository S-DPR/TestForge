package grpc_internal

import (
	"context"
	"github.com/redis/go-redis/v9"
	"google.golang.org/grpc"
	"log"
	"net"
	pb "rate-limit-service/grpc_internal/rate_limit_service"
	"rate-limit-service/internal/service"
)

var testExecutionLimit service.TestExecutionLimitService

type server struct {
	pb.UnimplementedLimitServer
}

func (s *server) TestExecutionLimit(ctx context.Context, req *pb.TestExecutionLimitReq) (*pb.TestExecutionLimitRes, error) {
	log.Printf("Received request: account_id=%s, count=%d", req.AccountId, req.Count)

	isLimit, accCount := testExecutionLimit.IsRateLimited(req.AccountId, req.Count)

	return &pb.TestExecutionLimitRes{
		IsLimit:  isLimit,
		AccCount: accCount,
	}, nil
}

func Serve() {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "",
		DB:       0,
	})
	testExecutionLimit = service.NewTestExecutionLimitService(ctx, rdb)

	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterLimitServer(s, &server{})

	log.Println("gRPC server listening on :50051")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
