#!/bin/bash
python3 /app/grpc/compile_grpc.py execution-service
python3 /app/execution-service/grpc_internal/server_v1.py &
python3 /app/execution-service/database_setup.py
#uvicorn main:app --host 0.0.0.0 --port 8002 --reload