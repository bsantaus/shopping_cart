install:
	pip install -r requirements.txt

start:
	docker compose up -d

kill:
	docker compose down

test:
	-docker stop postgres && docker rm postgres
	docker run --name postgres -p 5432:5432 -d --env-file .env postgres:latest
	export PYTHONPATH=$(shell pwd) && pytest tests/

