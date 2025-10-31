FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends netcat-openbsd \
#     && rm -rf /var/lib/apt/lists/*
COPY . .
RUN echo "RSI{suSsURRo_do_cem1t3rio_flag1}" > /app/flag1.txt && \
    chmod 444 /app/flag1.txt

USER root
EXPOSE 8080

CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "--bind", "0.0.0.0:8080", "app:app"]
