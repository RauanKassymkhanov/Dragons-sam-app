
.PHONY: install lint docker-up docker-down sam-build build-MyLayer

build-MyLayer:
	mkdir -p "$(ARTIFACTS_DIR)/python"
	poetry export -f requirements.txt --output "$(ARTIFACTS_DIR)/requirements.txt" --without-hashes
	pip install -r "$(ARTIFACTS_DIR)/requirements.txt" -t "$(ARTIFACTS_DIR)/python"

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
	sam build
