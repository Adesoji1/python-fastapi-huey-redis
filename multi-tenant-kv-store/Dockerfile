
FROM python:3.11.6-slim


WORKDIR /app


COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY .env /app/.env


ENV REDIS_HOST="redis"
ENV REDIS_PORT="6379"
ENV REDIS_DB="0"
ENV HUEY_REDIS_HOST="redis"
ENV HUEY_REDIS_PORT="6379"
ENV HUEY_REDIS_DB="1"


EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

