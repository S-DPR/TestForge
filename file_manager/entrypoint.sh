#!/bin/bash
python3 /app/grpc/compile_grpc.py file_manager
python3 /app/file_manager/grpc_ineternal/server_v1.py &
uvicorn main:app --host 0.0.0.0 --port 8001