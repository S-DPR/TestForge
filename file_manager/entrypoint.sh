#!/bin/bash
python3 /app/grpc/compile_grpc.py file_manager
python3 /app/file_manager/grpc/server_v1.py &
python3 /app/file_manager/main.py