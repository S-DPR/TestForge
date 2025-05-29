#!/bin/bash
python3 /app/grpc/compile_grpc.py auth
python3 -m grpc_internal.server_v1 &
python /app/auth/manage.py makemigrations
python /app/auth/manage.py migrate
python /app/auth/manage.py runserver 0.0.0.0:9000