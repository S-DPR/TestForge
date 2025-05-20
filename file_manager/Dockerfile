FROM python:3.13

WORKDIR /app

COPY ./file_manager /app/file_manager

COPY ./kafka_common /app/kafka_common

RUN pip install --no-cache-dir -r /app/file_manager/requirements.txt

RUN pip install -e /app/kafka_common

CMD ["python", "/app/file_manager/main.py"]