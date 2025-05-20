FROM python:3.13

WORKDIR /app/file_manager

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && pip install -e /app/kafka_common

COPY . .

CMD ["uvicorn", "file_manager.main:app", "--host", "0.0.0.0", "--port", "8000"]
