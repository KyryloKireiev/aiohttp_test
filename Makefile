.PHONY: setup \
		run \
		test \


PIP_VERSION = 22.3.1

venv/bin/activate: ## Alias for virtual environment
	python -m venv venv

setup: venv/bin/activate ## Project setup
	. venv/bin/activate; pip install pip==${PIP_VERSION} wheel setuptools
	. venv/bin/activate; pip install -r requirements.txt

run: venv/bin/activate ## Local Run
	. venv/bin/activate; python entry.py


