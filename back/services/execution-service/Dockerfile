FROM python:3.13

WORKDIR /app

COPY ./services/execution-service /app/execution-service

COPY ./libs/kafka_common /app/kafka_common

RUN pip install -r /app/execution-service/requirements.txt

RUN pip install -e /app/kafka_common

RUN chmod +x /app/execution-service/entrypoint.sh

CMD ["/app/execution-service/entrypoint.sh"]