FROM python:3.13

WORKDIR /app

COPY ./file_manager /app/file_manager

COPY ./kafka_common /app/kafka_common

RUN pip install -r /app/storage-service/requirements.txt

RUN pip install -e /app/kafka_common

RUN chmod +x /app/storage-service/entrypoint.sh

CMD ["/app/file_manager/entrypoint.sh"]