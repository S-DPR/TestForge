#!/bin/sh
set -e

PROTO_DIR="/app/grpc"
OUT_DIR="/app/gatekeeper-service/grpc_internal"

mkdir -p "$OUT_DIR"

protoc \
  --proto_path="$PROTO_DIR" \
  --go_out="$OUT_DIR" \
  --go-grpc_out="$OUT_DIR" \
  $(find "$PROTO_DIR" -name "*.proto")

cd /app/gatekeeper-service
cd /app/gatekeeper-service/cmd/server
go build -o /app/gatekeeper-service/main .

cd /app/gatekeeper-service
./main