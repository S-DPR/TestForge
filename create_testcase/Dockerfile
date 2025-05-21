FROM python:3.13

WORKDIR /app

COPY ./create_testcase /app/create_testcase

COPY ./kafka_common /app/kafka_common

RUN pip install --no-cache-dir -r /app/create_testcase/requirements.txt

RUN pip install -e /app/kafka_common

CMD ["python3", "/app/grpc/create_testcase/compile_grpc", "create_testcase", "v1"]

CMD ["python3", "/app/create_testcase/grec/server_v1.py"]

CMD ["python3", "/app/create_testcase/main.py"]