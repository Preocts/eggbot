.PHONY: update-deps init update install clean clean-pyc clean-build clean-test test package

update-deps:
	pip-compile --upgrade --generate-hashes
	pip-compile --upgrade --generate-hashes --output-file dev-requirements.txt dev-requirements.in

install:
	pip install --upgrade pip setuptools wheel
	pip install --upgrade -r requirements.txt  -r dev-requirements.txt
	pip install --editable .

init:
	pip install pip-tools
	rm -rf .tox

update: init update-deps install

# Run all cleaning steps
clean: clean-build clean-pyc clean-test

clean-pyc: ## Remove python artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build: ## Remove build artifacts.
	rm -f artifact.zip
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf vendors/
	rm -rf lambda-artifact.zip
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-test: ## Remove test artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	find . -name '.pytest_cache' -exec rm -fr {} +

blacken: ## Run Black against code
	black --line-length 79 ./src/eggbot
	black --line-length 79 ./tests

test: ## Run all tests found in the /tests directory.
	coverage run -m pytest tests/
	coverage report --include "*/eggbot/*" --show-missing

package: clean-build ## Creates a package for testing
	mkdir vendors
	mkdir dist
	pip install -r requirements.txt -t ./vendors
	cp -r vendors/* ./dist/
	cp -r ./src/eggbot ./dist
	cp -r ./config/ ./dist/
	mv ./dist/eggbot/__main__.py ./dist/main.py
	(cd ./dist && zip -r ../artifact.zip .)
