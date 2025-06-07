#!/bin/bash
python3 /app/grpc/compile_grpc.py orchestrator
python3 /app/orchestrator/grpc_internal/server_v1.py &
#uvicorn main:app --host 0.0.0.0 --port 8003 --reload