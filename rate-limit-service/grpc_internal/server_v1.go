package grpc_internal

import (
	"context"
	"github.com/redis/go-redis/v9"
	"log"
	pb "rate-limit-service/grpc_internal/rate_limit_service"
	"rate-limit-service/internal/service"
)

var testExecutionLimit service.TestExecutionLimitService

type server struct {
	pb.UnimplementedFileServer
}

func (s *server) FileSave(ctx context.Context, req *pb.TestExecutionLimitReq) (*pb.TestExecutionLimitRes, error) {
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
}
