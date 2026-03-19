#!/usr/bin/env sh
set -e

docker compose -f docker-compose.base.yml -f docker-compose.video.yml -f docker-compose.devtools.yml logs -f
