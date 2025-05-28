#!/bin/bash
python3 /app/grpc/compile_grpc.py create_testcase
python3 /app/create_testcase/grpc_internal/server_v1.py &
python3 /app/create_testcase/database_setup.py
uvicorn main:app --host 0.0.0.0 --port 8000 --reload