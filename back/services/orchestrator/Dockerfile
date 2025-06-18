FROM python:3.13

WORKDIR /app

COPY ./services/orchestrator /app/orchestrator

COPY ./libs/kafka_common /app/kafka_common

COPY ./libs/log_common /app/log_common

RUN pip install -r /app/orchestrator/requirements.txt

RUN pip install -e /app/kafka_common

RUN pip install -e /app/log_common

RUN chmod +x /app/orchestrator/entrypoint.sh

CMD ["/app/orchestrator/entrypoint.sh"]