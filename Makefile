.PHONY: setup \
		run \
		test \
		flake8\
		isort\
		black\
		migration\
		migrate\
		downgrate\


PIP_VERSION = 22.3.1

venv/bin/activate: ## Alias for virtual environment
	python -m venv venv

setup: venv/bin/activate ## Project setup
	. venv/bin/activate; pip install pip==${PIP_VERSION} wheel setuptools
	. venv/bin/activate; pip install -r requirements.txt

run: venv/bin/activate ## Local Run
	. venv/bin/activate; python entry.py

flake8: venv/bin/activate ## Run flake8
	. venv/bin/activate; flake8 ./api_demo/

isort: venv/bin/activate ## Run isort
	. venv/bin/activate; isort ./api_demo/

black: venv/bin/activate ## Run black
	. venv/bin/activate; black ./api_demo/

migration: venv/bin/activate ## Make migration
	. venv/bin/activate; alembic revision --autogenerate

db: venv/bin/activate ## Run migration
	. venv/bin/activate; alembic upgrade head

downgrade: venv/bin/activate ## Revert the last applied migration
	. venv/bin/activate; alembic downgrade -1

test: venv/bin/activate ## Run tests
	. venv/bin/activate; pytest
