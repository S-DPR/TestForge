package grpc_internal

import (
	"context"
	pb "gatekeeper-service/grpc_internal/gatekeeper_service"
	"gatekeeper-service/internal/service"
	"google.golang.org/grpc"
	"log"
	"net"
)

var jwtAuthService *service.JwtAuthzService

type server struct {
	pb.UnimplementedGatekeeperServer
}

func (s *server) TestExecutionLimit(ctx context.Context, req *pb.ValidateJwtReq) (*pb.ValidateJwtRes, error) {
	log.Printf("Received request: account_id=%s, count=%d", req.AccessToken)

	accountId := jwtAuthService.JWTAuth(req.AccessToken)

	return &pb.ValidateJwtRes{
		AccountId: accountId,
	}, nil
}

func Serve() {
	jwtAuthService = service.NewJwtAuthzService()

	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterGatekeeperServer(s, &server{})

	log.Println("gRPC server listening on :50051")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
