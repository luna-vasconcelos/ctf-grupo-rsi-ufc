FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

COPY . .

# RUN useradd --create-home --uid 10001 appuser && \
#     mkdir -p /flags && \
#     chown -R appuser:appuser /app /flags

# RUN printf '%s\n' '#!/bin/sh' \
#     'set -eu' \
#     '[ -n "${FLAG1:-}" ] && printf "%s" "$FLAG1" > /flag1.txt && chmod 444 /flag1.txt || true' \
#     'exec "$@"' \
#     > /docker-entrypoint.sh && chmod +x /docker-entrypoint.sh

RUN echo "RSI{suSsUrro_do_cem1t3rio_flag1}" > /flag1.txt

USER appuser
EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "--bind", "0.0.0.0:8080", "app:app"]
