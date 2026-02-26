.PHONY: up down logs test

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

test:
	docker compose run --rm -e MONGO_DB=shop_test api pytest -q
