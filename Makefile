.PHONY: help test init

dc = docker-compose -f $(YML)
run = $(dc) run --rm stockinfo_django_local
manage = $(run) python manage.py
pytest = $(run) pytest --timeout=5 --cov --cov-fail-under=90 $(ARGS)

init: clean build migrate           ## Init clean

help:                               ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:
	pip install -r requirements/local.txt

migrations:                         ## Make migrations
	$(manage) makemigrations $(ARGS)

migrate:                            ## Migrate
	$(manage) migrate

urls:                               ## Show URL endpoints
	$(manage) show_urls

superuser:                          ## Create a superuser (user with admin rights)
	$(manage) createsuperuser

env:                                ## Print current env
	env | sort

run:                                ## Run in local Docker container
	$(dc) up

stop:                               ## Run in local Docker container
	$(dc) stop

clean:                              ## Clean docker stuff
	$(dc) down -v --remove-orphans

build:                              ## Build docker image
	$(dc) build

status:                             ## Show container status
	$(dc) ps

run-command:                        ## Run a manage.py command
	$(manage) $(ARGS)

unittest:                           ## Run all unit tests in a container (report to terminal)
	$(pytest) --cov-report term

unittest-html:                      ## Run all unit tests in a container (report as html)
	$(pytest) --cov-report html

functionaltest:                     ## Run automated functional tests (*outside* of container)
	pytest --cov --cov-report term --cov-fail-under=95 cantor_stockinfo/tests/functional_tests.py

unittest-local:                     ## Run all unit tests (*outside* of container)
	pytest --cov --cov-report term --cov-fail-under=90 --timeout=5

generate-key:                       ## Generate a new Django secret key
	python manage.py shell -c "from django.core.management import utils; print(utils.get_random_secret_key())"
