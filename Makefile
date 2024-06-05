install:
	pip install -r requirements.txt

build:
	cp .env.compose .env
	docker build . -t shopping_cart_api:latest

start-local-api:
	cp .env.test .env
	fastapi run main.py

start: build
	cp .env.compose .env
	docker compose up --force-recreate -d

kill:
	cp .env.compose .env
	docker compose down

start-db:
	docker run --name postgres -p 5432:5432 -d --env-file .env.test postgres:latest
	sleep 2

kill-db:
	docker stop postgres && docker rm postgres

_test:
	cp .env.test .env
	export PYTHONPATH=$(shell pwd) && pytest tests/

test: start-db _test kill-db
	

