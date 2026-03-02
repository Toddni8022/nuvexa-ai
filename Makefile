.PHONY: help setup install test lint format type-check run docker-build docker-up clean

PYTHON ?= python
PIP    ?= pip

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

setup: ## Install all dependencies (including dev)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov ruff mypy

install: ## Install runtime dependencies only
	$(PIP) install -r requirements.txt

test: ## Run the test suite
	$(PYTHON) -m pytest tests/ -v --cov=. --cov-report=term-missing

test-fast: ## Run tests without coverage
	$(PYTHON) -m pytest tests/ -q

lint: ## Run ruff linter
	$(PYTHON) -m ruff check .

format: ## Format code with ruff
	$(PYTHON) -m ruff format .

type-check: ## Run mypy type checker
	$(PYTHON) -m mypy app.py assistant.py database.py shopping.py config.py

run: ## Start the NUVEXA application
	$(PYTHON) -m streamlit run app.py

docker-build: ## Build the Docker image
	docker build -t nuvexa-ai .

docker-up: ## Start all services with Docker Compose
	docker compose up --build

docker-down: ## Stop Docker Compose services
	docker compose down

clean: ## Remove build artifacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
