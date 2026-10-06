.PHONY: install run test lint docker-up

install:
	uv sync

run:
	uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

docker-up:
	docker compose up --build
