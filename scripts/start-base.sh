#!/usr/bin/env sh
set -e

docker compose --env-file .env -f docker-compose.base.yml up -d --build
