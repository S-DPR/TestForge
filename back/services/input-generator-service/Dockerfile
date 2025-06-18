FROM python:3.13

WORKDIR /app

COPY ./services/input-generator-service /app/input-generator-service

COPY ./libs/kafka_common /app/kafka_common

COPY ./libs/log_common /app/log_common

RUN pip install -r /app/input-generator-service/requirements.txt

RUN pip install -e /app/kafka_common

RUN pip install -e /app/log_common

RUN chmod +x /app/input-generator-service/entrypoint.sh

CMD ["/app/input-generator-service/entrypoint.sh"]