.PHONY: lint format typecheck test test-cov install clean

install:
	poetry install

lint:
	pre-commit run --all-files

format:
	black .
	isort .

typecheck:
	mypy src tests

test:
	pytest tests/

test-cov:
	pytest --cov=src --cov-report=html tests/

clean:
	rm -rf .coverage htmlcov

all: lint typecheck test
