# Makefile for {{ cookiecutter.project_name }}

SRC_DIRS := src tests

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

# Setup
.PHONY: install
install: ## Install all dependency groups
	uv sync --all-groups

# Run
.PHONY: run serve notebook
run: ## Ask the agent a question: make run Q="What time is it?"
	uv run {{ cookiecutter.project_slug }} "$(Q)"

serve: ## Start the API with auto-reload on http://127.0.0.1:8000 (docs at /docs)
	uv run uvicorn {{ cookiecutter.module_name }}.api:app --reload

notebook: ## Launch Jupyter Lab
	uv run --with jupyterlab jupyter lab

# Code quality
.PHONY: lint format typecheck check
lint: ## Run ruff linter
	uv run ruff check $(SRC_DIRS)

format: ## Format code with ruff
	uv run ruff format $(SRC_DIRS)

typecheck: ## Run mypy
	uv run mypy $(SRC_DIRS)

check: format lint typecheck ## Format, lint and type-check

# Tests
.PHONY: test test-cov
test: ## Run tests (offline: they use a fake LLM)
	uv run pytest

test-cov: ## Run tests with a line-by-line coverage report
	uv run pytest --cov-report=term-missing

# Cleanup
.PHONY: clean
clean: ## Remove caches and build artifacts
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
