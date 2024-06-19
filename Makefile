#!make
include .env
export

DOCKER_COMPOSE=docker-compose -f ./docker/docker-compose.yml --project-directory=./docker
DOCKER_EXEC=docker exec ${PROJECT_NAME}.php-fpm

CURRENT_UID := $(shell id -u)
CURRENT_USER := $(shell whoami)

export CURRENT_UID
export CURRENT_USER

.PHONY: init
init: build up composer optimize

.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

.PHONY: down
down:
	$(DOCKER_COMPOSE) down

.PHONY: build
build:
	$(DOCKER_COMPOSE) build --force-rm

.PHONY: composer
composer:
	$(DOCKER_EXEC) composer install -n

.PHONY: optimize
optimize:
	$(DOCKER_EXEC) php artisan cache:clear
	$(DOCKER_EXEC) php artisan optimize
	$(DOCKER_EXEC) php artisan storage:link

.PHONY: exec
exec:
	docker exec -it ${PROJECT_NAME}.php-fpm bash
