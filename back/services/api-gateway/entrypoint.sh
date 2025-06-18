#!/bin/sh
set -e

PROTO_DIR="/app/grpc"
OUT_DIR="/app/api-gateway/grpc_internal"

mkdir -p "$OUT_DIR"

protoc \
  --proto_path="$PROTO_DIR" \
  --go_out="$OUT_DIR" \
  --go-grpc_out="$OUT_DIR" \
  $(find "$PROTO_DIR" -name "*.proto")

cd /app/api-gateway
cd /app/api-gateway/cmd/server
go build -o /app/api-gateway/main .

cd /app/api-gateway
./main