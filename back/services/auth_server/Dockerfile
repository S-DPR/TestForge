FROM python:3.13

WORKDIR /app

COPY ./services/auth_server /app/auth_server

COPY ./libs/kafka_common /app/kafka_common

RUN pip install -r /app/auth_server/requirements.txt

RUN pip install -e /app/kafka_common

RUN chmod +x /app/auth_server/entrypoint.sh

CMD ["/app/auth_server/entrypoint.sh"]
