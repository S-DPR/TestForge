#!/bin/bash
python3 /app/grpc/compile_grpc.py auth
python3 /app/auth/grpc_internal/server_v1.py &
python /app/auth/manage.py makemigrations
python /app/auth/manage.py migrate
python /app/auth/manage.py runserver 0.0.0.0:9000