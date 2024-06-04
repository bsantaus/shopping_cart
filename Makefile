install:
	pip install -r requirements.txt

start-dev-db:
	docker run -d --env-file .env -p 5432:5432 postgres:latest

start-dev-app:
	fastapi dev main.py

test:
	export PYTHONPATH=$(shell pwd) && pytest tests/

