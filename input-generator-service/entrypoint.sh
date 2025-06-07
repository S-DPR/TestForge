#!/bin/bash
python3 /app/grpc/compile_grpc.py input-generator-service
python3 /app/input-generator-service/grpc_internal/server_v1.py &
python3 /app/input-generator-service/database_setup.py
#uvicorn main:app --host 0.0.0.0 --port 8000 --reload