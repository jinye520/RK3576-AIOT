#!/usr/bin/env sh
set -e

docker compose --env-file .env -f docker-compose.base.yml up -d --build
docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.video.yml up -d
docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.devtools.yml up -d
