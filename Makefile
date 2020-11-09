.PHONY: clean-pyc clean-build venv dependancies

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

venv:
	python3.8 -m venv venv

dependancies:
	pip install --upgrade pip
	pip install --upgrade setuptools
	pip install --upgrade wheel
	pip install -r requirements.txt

dev-dependancies:
	pip install -r dev-requirements.txt