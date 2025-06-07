#!/bin/bash
python3 /app/grpc/compile_grpc.py storage-service
python3 /app/storage-service/grpc_internal/server_v1.py &
#uvicorn main:app --host 0.0.0.0 --port 8001