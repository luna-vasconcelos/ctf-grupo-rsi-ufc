FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN printf '%s\n' \
  '#!/bin/sh' \
  'PORT_FILE="${PORT_FILE:-/run/tcpchat/port}"' \
  'DESIRED_FILE="${DESIRED_FILE:-/run/tcpchat/desired}"' \
  '' \
  'if [ -n "${1:-}" ]; then' \
  '  REQ="$1"' \
  '  case "$REQ" in (*[!0-9]*|"") echo "Invalid port: $REQ" >&2; exit 2;; esac' \
  '  printf "%s" "$REQ" > "$DESIRED_FILE"' \
  '  # wait up to ~5s for tcpchat to publish the requested port' \
  '  for i in 1 2 3 4 5 6 7 8 9 10; do' \
  '    CUR="$(cat "$PORT_FILE" 2>/dev/null || true)"' \
  '    [ "$CUR" = "$REQ" ] && break' \
  '    sleep 0.5' \
  '  done' \
  '  exec nc tcpchat "$REQ"' \
  'else' \
  '  CUR="$(cat "$PORT_FILE")"' \
  '  exec nc tcpchat "$CUR"' \
  'fi' \
  > /usr/local/bin/nc-tcpchat && chmod +x /usr/local/bin/nc-tcpchat

COPY . .

RUN echo "RSI{suSsURRo_do_cem1t3rio_flag1}" > /app/flag1.txt && \
    chmod 444 /app/flag1.txt

USER root
EXPOSE 8080

CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "--bind", "0.0.0.0:8080", "app:app"]
