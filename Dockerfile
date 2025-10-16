# Dockerfile ajustado
FROM python:3.11-slim
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY ./app /app
RUN mkdir -p /app/static /data && pip install --no-cache-dir fastapi uvicorn jinja2 python-multipart
VOLUME ["/data"]
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
