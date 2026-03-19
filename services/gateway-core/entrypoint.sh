#!/usr/bin/env sh
set -e

if [ ! -f /app/config.json ] && [ -f /app/config.example.json ]; then
  cp /app/config.example.json /app/config.json
  echo '[gateway-core] config.json created from config.example.json'
fi

exec python /app/main.py --config /app/config.json
