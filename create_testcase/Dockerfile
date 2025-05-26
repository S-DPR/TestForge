FROM python:3.13

WORKDIR /app

COPY ./create_testcase /app/create_testcase

COPY ./kafka_common /app/kafka_common

RUN pip install -r /app/create_testcase/requirements.txt

RUN pip install -e /app/kafka_common

RUN chmod +x /app/create_testcase/entrypoint.sh

CMD ["/app/create_testcase/entrypoint.sh"]