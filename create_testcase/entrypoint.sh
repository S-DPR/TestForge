#!/bin/bash
python3 /app/grpc/compile_grpc.py create_testcase v1
python3 /app/create_testcase/grpc/server_v1.py &
python3 /app/create_testcase/main.py