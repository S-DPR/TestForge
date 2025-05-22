#!/bin/bash
python3 /app/grpc/compile_grpc.py orchestrator
uvicorn main:app --host 0.0.0.0 --port 8003