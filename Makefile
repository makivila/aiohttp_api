#!make
include .env

migrate_revision:
	docker exec -it aiohttp_app alembic revision --autogenerate

migrate_up:
	docker exec -it aiohttp_app alembic upgrade head

migrate_down:
	docker exec -it aiohttp_app alembic downgrade -1

run:
	docker-compose up -d --build

stop:
	docker-compose stop

logs:
	docker-compose logs -f