# Используем официальный Python образ
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p backups logs
RUN useradd -m -r nornir-user && \
    chown -R nornir-user:nornir-user /app
USER nornir-user
ENV PYTHONPATH=/app
ENV NORNIR_CONFIG=/app/config/nornir_config.yaml
CMD ["python", "scripts/check_status.py"] 