#!/bin/bash
python3 /app/grpc/create_testcase/compile_grpc create_testcase v1
python3 /app/create_testcase/grec/server_v1.py &
python3 /app/create_testcase/main.py