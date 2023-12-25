.PHONY: install test lint

install:
	@echo "\nInstalling dependencies..."
	@python -m pip install --upgrade pip
	@python -m pip install -e .
	@echo "Done."

dev: install
	@echo "\nInstalling development dependencies..."
	@python -m pip install -e ".[dev]"
	@echo "Done."

test:
	@echo "\nRunning tests..."
	@python -m pytest -v
	@echo "Done."

lint:
	@echo "\nRunning Mypy..."
	@mypy . --ignore-missing-imports
	@echo "\nRunning Black Checker..."
	@black --check .

clean:
	@echo "Cleaning up..."
	@rm -rf .ipynb_checkpoints
	@rm -rf **/.ipynb_checkpoints
	@rm -rf .pytest_cache
	@rm -rf **/.pytest_cache
	@rm -rf __pycache__
	@rm -rf **/__pycache__
	@rm -rf src/*.egg-info
	@rm -rf .mypy_cache
	@rm -rf dist 
	@echo "Done."
