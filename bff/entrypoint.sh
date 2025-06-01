#!/bin/sh
set -e

PROTO_DIR="/app/grpc"
OUT_DIR="/app/bff/grpc_internal"

mkdir -p "$OUT_DIR"

protoc \
  --proto_path="$PROTO_DIR" \
  --go_out="$OUT_DIR" \
  --go-grpc_out="$OUT_DIR" \
  $(find "$PROTO_DIR" -name "*.proto")

cd /app/bff
cd /app/bff/cmd/server
go build -o /app/bff/main .

cd /app/bff
./main