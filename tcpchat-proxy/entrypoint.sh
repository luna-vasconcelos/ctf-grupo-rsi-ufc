#!/bin/sh
set -eu

PORT_FILE=${PORT_FILE:-/run/tcpchat/port}
DESIRED_FILE=${DESIRED_FILE:-/run/tcpchat/desired}
TARGET_HOST=${TARGET_HOST:-tcpcore}
TARGET_PORT=${TARGET_PORT:-1337}
ROTATE_SECS=${ROTATE_SECS:-20}

mkdir -p "$(dirname "$PORT_FILE")"
: > "$DESIRED_FILE"          
chmod 666 "$DESIRED_FILE"    
chmod 644 "$PORT_FILE" 2>/dev/null || true

while :; do
  USE_DESIRED=0
  PORT=""
  if [ -s "$DESIRED_FILE" ]; then
    PORT="$(tr -cd '0-9' < "$DESIRED_FILE" | head -c 5 || true)"
    [ -n "$PORT" ] && USE_DESIRED=1
  fi
  [ -z "$PORT" ] && PORT="$(shuf -i 20000-40000 -n 1)"

  printf '%s' "$PORT" > "$PORT_FILE"
  echo "$(date +%T) tcpchat listening on $PORT -> $TARGET_HOST:$TARGET_PORT"

  socat TCP-LISTEN:"$PORT",fork,reuseaddr TCP:"$TARGET_HOST":"$TARGET_PORT" &
  PID=$!

  [ "$USE_DESIRED" = 1 ] && : > "$DESIRED_FILE"

  SECS=0
  while [ $SECS -lt "$ROTATE_SECS" ]; do
    sleep 1; SECS=$((SECS+1))
    if [ -s "$DESIRED_FILE" ]; then
      NEW="$(tr -cd '0-9' < "$DESIRED_FILE" | head -c 5 || true)"
      [ -n "$NEW" ] && [ "$NEW" != "$PORT" ] && break
    fi
  done

  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
done
