.PHONY: ps clean help up down restart build rebuild logs logs-all shell migrate

help:
	@echo ""
	@echo "DevOps Platform"
	@echo "========================="
	@echo "make ps        	Containers list"
	@echo "make clean     	Delete all containers and volumes"
	@echo "make up        	Start containers"
	@echo "make down      	Stop containers"
	@echo "make build     	Build images"
	@echo "make rebuild   	Rebuild images"
	@echo "make logs      	Backend logs"
	@echo "make logs-all  	All logs"
	@echo "make shell     	Backend shell"
	@echo "make migrate   	Run migrations"
	@echo "make revision   	Create migrations"

ps:
	docker compose ps

env:
	docker compose config

clean:
	docker compose down -v

up:
	docker compose up -d

down:
	docker compose down

restart: 
	docker compose down
	docker compose up -d

build:
	docker compose build

rebuild:
	docker compose build --no-cache
	docker compose up -d

logs:
	docker compose logs -f backend

logs-all:
	docker compose logs -f

shell: 
	docker compose exec backend bash

migrate:
	docker compose exec backend alembic upgrade head

revision:
ifndef MSG
	$(error MSG is required. Example: make revision MSG=create_users_table)
endif
	docker compose exec backend alembic revision --autogenerate -m "$(MSG)"