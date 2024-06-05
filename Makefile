install:
	pip install -r requirements.txt

start:
	docker compose up -d

kill:
	docker compose down

start-db:
	docker run --name postgres -p 5432:5432 -d --env-file .env postgres:latest
	sleep 2

kill-db:
	docker stop postgres && docker rm postgres

_test:
	export PYTHONPATH=$(shell pwd) && pytest tests/

test: start-db _test kill-db
	

