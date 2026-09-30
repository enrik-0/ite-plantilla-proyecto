.PHONY: install test lint coverage docker-up docker-down db-migrate db-seed clean

install:
	uv sync --project backend
	cd frontend && pnpm install

test:
	uv run --project backend pytest backend/tests
	cd frontend && pnpm test

lint:
	uv run --project backend ruff check backend
	cd frontend && pnpm lint

coverage:
	uv run --project backend pytest --cov=backend/src backend/tests
	cd frontend && pnpm coverage

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

db-migrate:
	uv run --project backend alembic -c backend/alembic.ini upgrade head

db-seed:
	uv run --project backend python -m src.db.seed

clean:
	rm -rf backend/.pytest_cache backend/.ruff_cache frontend/node_modules frontend/dist
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
