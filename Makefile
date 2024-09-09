
.PHONY: install lint docker-up docker-down sam-build

install:
	poetry install

lint:
	poetry run ruff check .
	poetry run ruff check . --fix

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down -v

sam-build:
	sam build --template-file Dragons-sam-app/template.yaml
