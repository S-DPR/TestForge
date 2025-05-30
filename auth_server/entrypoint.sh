#!/bin/bash
python3 /app/grpc/compile_grpc.py auth_server
python3 /app/auth_server/grpc_internal/server_v1.py &
python /app/auth_server/manage.py makemigrations
python /app/auth_server/manage.py migrate
python /app/auth_server/manage.py runserver 0.0.0.0:9000