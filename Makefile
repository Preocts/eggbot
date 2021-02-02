.PHONY: dev-install clean clean-pyc clean-build clean-test tests package

dev-install:
	pip install --upgrade pip setuptools wheel
	pip install --upgrade -r requirements.txt  -r dev-requirements.txt

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

tests: ## Run all tests found in the /tests directory.
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
