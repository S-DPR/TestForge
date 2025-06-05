#!/bin/sh
set -e

PROTO_DIR="/app/grpc"
OUT_DIR="/app/rate-limit-service/grpc_internal"

mkdir -p "$OUT_DIR"

protoc \
  --proto_path="$PROTO_DIR" \
  --go_out="$OUT_DIR" \
  --go-grpc_out="$OUT_DIR" \
  $(find "$PROTO_DIR" -name "*.proto")

cd /app/rate-limit-service
cd /app/rate-limit-service/cmd/server
go build -o /app/rate-limit-service/main .

cd /app/rate-limit-service
./main