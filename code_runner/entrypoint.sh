#!/bin/bash
python3 /app/grpc/compile_grpc.py code_runner
python3 /app/code_runner/grpc_internal/server_v1.py &
uvicorn main:app --host 0.0.0.0 --port 8002