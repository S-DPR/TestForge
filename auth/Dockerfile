FROM python:3.13

WORKDIR /app

COPY ./auth /app/auth

COPY ./kafka_common /app/kafka_common

RUN pip install -r /app/auth/requirements.txt

RUN pip install -e /app/kafka_common

RUN chmod +x /app/auth/entrypoint.sh

CMD ["/app/auth/entrypoint.sh"]
