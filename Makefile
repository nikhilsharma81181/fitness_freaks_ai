.PHONY: dev start clean build test

dev:
	python -m src.main

start:
	python -m src.main

build:
	@echo "Building project..."
	@# Add build steps here if needed

clean:
	@echo "Cleaning project..."
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

test:
	@echo "Running tests..."
	@# Add test command here, e.g. pytest

install:
	pip install -r requirements.txt

help:
	@echo "Available commands:"
	@echo "  make dev       - Run the development server with auto-reload"
	@echo "  make start     - Start the server"
	@echo "  make build     - Build the project"
	@echo "  make clean     - Clean cached Python files"
	@echo "  make test      - Run tests"
	@echo "  make install   - Install dependencies" 