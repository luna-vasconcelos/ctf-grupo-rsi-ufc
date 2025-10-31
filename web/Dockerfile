FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /web

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends netcat-openbsd \
#     && rm -rf /var/lib/apt/lists/*

COPY . .

<<<<<<< HEAD
# --- CORREÇÃO AQUI ---

# 1. Crie a flag COMO ROOT durante o build. O arquivo já existirá no contêiner.
RUN echo "RSI{suSsUrro_do_cem1t3rio_flag1}" > /flag1.txt && \
    chmod 444 /flag1.txt

# 2. Crie o entrypoint.sh, mas agora ele só precisa executar o comando.
RUN printf '%s\n' '#!/bin/sh' \
    'set -eu' \
    'exec "$@"' \
    > /docker-entrypoint.sh && chmod +x /docker-entrypoint.sh

# 3. Crie o usuário
RUN useradd -m appuser

# 4. Mude para o usuário
USER appuser

EXPOSE 8080

# 5. Defina o ponto de entrada (que agora existe e fará a coisa certa)
ENTRYPOINT ["/docker-entrypoint.sh"]

# Comando padrão a ser executado pelo entrypoint
=======
RUN echo "RSI{suSsURRo_do_cem1t3rio_flag1}" > /app/flag1.txt && \
    chmod 444 /app/flag1.txt

USER root
EXPOSE 8080

>>>>>>> origin/updates-containers
CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "--bind", "0.0.0.0:8080", "app:app"]
