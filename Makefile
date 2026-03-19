ENV_FILE=.env
BASE=docker-compose.base.yml
VIDEO=docker-compose.video.yml
DEVTOOLS=docker-compose.devtools.yml

.PHONY: base-up video-up devtools-up all-up down logs ps

base-up:
	docker compose --env-file $(ENV_FILE) -f $(BASE) up -d --build

video-up:
	docker compose --env-file $(ENV_FILE) -f $(BASE) -f $(VIDEO) up -d

devtools-up:
	docker compose --env-file $(ENV_FILE) -f $(BASE) -f $(DEVTOOLS) up -d --build

all-up:
	docker compose --env-file $(ENV_FILE) -f $(BASE) up -d --build
	docker compose --env-file $(ENV_FILE) -f $(BASE) -f $(VIDEO) up -d
	docker compose --env-file $(ENV_FILE) -f $(BASE) -f $(DEVTOOLS) up -d --build

down:
	docker compose -f $(BASE) -f $(VIDEO) -f $(DEVTOOLS) down

logs:
	docker compose -f $(BASE) logs -f

ps:
	docker compose -f $(BASE) -f $(VIDEO) -f $(DEVTOOLS) ps
