FROM python:3.13

WORKDIR /app

COPY ./code_runner /app/code_runner

COPY ./kafka_common /app/kafka_common

RUN pip install --no-cache-dir -r /app/code_runner/requirements.txt

RUN pip install -e /app/kafka_common

RUN chmod +x /app/code_runner/entrypoint.sh

CMD ["/app/code_runner/entrypoint.sh"]