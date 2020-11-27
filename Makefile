.PHONY: dependancies clean

# Install requirement packages for development
dependancies:
	pip install --upgrade pip
	pip install --upgrade setuptools
	pip install --upgrade wheel
	pip install -r requirements.txt

# Install development packages for linting and tests
dev-dependancies:
	pip install -r dev-requirements.txt

# Run all cleaning steps
clean: clean-build clean-pyc clean-test

# Remove build artifacts
clean-build:
	rm -f artifact.zip
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

# Remove pyc artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# Remove test artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

# Creates a package for testing
package: clean-build
	mkdir dist
	pip install -r requirements.txt -t ./dist
	cp -r ./src/eggbot/* ./dist
	test -f ./src/eggbot/.env && cp ./src/eggbot/.env ./dist/.env
	(cd ./dist && zip -r ../artifact.zip .)

# Run tests
run-test:
	python -m unittest discover -s tests