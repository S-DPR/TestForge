FROM python:3.13

WORKDIR /app

COPY ./create_testcase /app/create_testcase

COPY ./kafka_common /app/kafka_common

RUN pip install --no-cache-dir -r /app/create_testcase/requirements.txt

RUN pip install -e /app/kafka_common

CMD ["uvicorn", "create_testcase.main:app", "--host", "0.0.0.0", "--port", "8000"]