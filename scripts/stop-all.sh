#!/usr/bin/env sh
set -e

docker compose -f docker-compose.base.yml -f docker-compose.video.yml down
