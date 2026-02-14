# Используем официальный образ Python 3.13
FROM python:3.13-slim

# Установка uv (быстрый pip)
ENV PATH="/root/.local/bin:${PATH}"
RUN pip install --no-cache-dir 'uv>=0.5.0' && \
    rm -rf /root/.cache/pip

# Рабочая директория
WORKDIR /app

# Копируем pyproject.toml и устанавливаем зависимости
COPY pyproject.toml .
RUN uv pip install --system . && \
    uv cache prune

# Копируем исходники бэкенда
COPY src/ src/

# Копируем frontend (просто статика) в папку static
COPY frontend/ src/static/

# Healthcheck — проверяем API
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Открываем порт
EXPOSE 8000

# Запуск приложения: Gunicorn + UvicornWorker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "src.main:app"]
