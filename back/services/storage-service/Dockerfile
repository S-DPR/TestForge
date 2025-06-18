FROM python:3.13

WORKDIR /app

COPY ./storage-service /app/storage-service

COPY ./kafka_common /app/kafka_common

RUN pip install -r /app/storage-service/requirements.txt

RUN pip install -e /app/kafka_common

RUN chmod +x /app/storage-service/entrypoint.sh

CMD ["/app/storage-service/entrypoint.sh"]