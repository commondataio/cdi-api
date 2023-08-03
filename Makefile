
all:
	make api

build:
	docker build -t ghcr.io/commondataio/cdiapi:latest .

shell: build
	docker-compose run --rm app bash

services:
	docker-compose up --remove-orphans -d index

api: build services
	docker-compose up --remove-orphans app

unit-test:
	pytest -v tests/unit

integration-test:
	pytest -v tests/integration

typecheck:
	mypy --strict cdiapi

check: typecheck integration-test unit-test