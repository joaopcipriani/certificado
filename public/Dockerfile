FROM python:3.11-slim

# Instala OpenSSL e dependências
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

# Cria diretórios
WORKDIR /app
COPY ./app /app

# Instala dependências Python
RUN pip install --no-cache-dir fastapi uvicorn jinja2 python-multipart

# Pasta compartilhada para saída
VOLUME ["/data"]

# Porta da API
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
