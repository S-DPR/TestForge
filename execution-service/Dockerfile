FROM python:3.13

WORKDIR /app

COPY ./code_runner /app/code_runner

COPY ./kafka_common /app/kafka_common

RUN pip install -r /app/execution-service/requirements.txt

RUN pip install -e /app/kafka_common

RUN chmod +x /app/execution-service/entrypoint.sh

CMD ["/app/code_runner/entrypoint.sh"]