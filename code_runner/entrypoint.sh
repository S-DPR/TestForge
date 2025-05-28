#!/bin/bash
python3 /app/grpc/compile_grpc.py code_runner
python3 /app/code_runner/grpc_internal/server_v1.py &
python3 /app/code_runner/database_setup.py
uvicorn main:app --host 0.0.0.0 --port 8002 --reload