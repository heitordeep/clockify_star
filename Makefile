#!/bin/bash

SHELL=/bin/bash

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

# ------ Code style ------

style:  ## Run isort and black auto formatting code style in the project.
	@isort -m 3 -tc -y
	@black -S -t py37 -l 79 . --exclude '/(\.git|\.venv|env|venv|build|dist)/'

style-check:  ## Check isort and black code style.
	@black -S -t py37 -l 79 --check . --exclude '/(\.git|\.venv|env|venv|build|dist)/'

clean:  ## Clean python bytecodes, optimized files, cache, coverage...
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".cache" -type d | xargs rm -rf
	@find . -name ".coverage" -type f | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@echo 'Temporary files deleted'

# ------ Installation requirements ------ 

requirements: ## Install project packages.
	@pip install --upgrade pip
	@pip install -r requirements/requirements_dev.txt 

# -------- Docker ---------
pull:
	@docker pull puckel/docker-airflow

run:
	@docker run -d -p 8080:8080 -v /opt/airflow/dags:/usr/local/airflow/dags -v /opt/airflow/clockify:/usr/local/airflow puckel/docker-airflow webserver

access:
	@docker exec -it job-clockify bash

# -------- App ------------

run: clean ## Post hours in the clockify.
	@python main.py $(args)

get_param: clean ## Update files job.
	@python clockify_app/get_parameters_api.py $(id)
