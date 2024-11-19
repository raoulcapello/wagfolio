.DEFAULT_GOAL := help

# Docker settings
DOCKER_COMPOSE_YAML = docker-compose.local.yml
APP_SERVICE = django

# Docker commands
dc = docker-compose -f $(DOCKER_COMPOSE_YAML)
run = $(dc) run --rm $(APP_SERVICE)
manage = python manage.py
pytest = $(run) pytest --timeout=5 --cov --cov-fail-under=90 $(ARGS)


.PHONY: help
help:                               ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

.PHONY: clean-coverage
clean-coverage: ## Remove coverage reports
	@echo "+ $@"
	@rm -rf htmlcov/
	@rm -rf .coverage
	@rm -rf coverage.xml

.PHONY: clean-pytest
clean-pytest: ## Remove pytest cache
	@echo "+ $@"
	@rm -rf .pytest_cache/

.PHONY: clean-docs-build
clean-docs-build: ## Remove local docs
	@echo "+ $@"
	@rm -rf docs/_build

.PHONY: clean-build
clean-build: ## Remove build artifacts
	@echo "+ $@"
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

.PHONY: clean-pyc
clean-pyc: ## Remove Python file artifacts
	@echo "+ $@"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

clean-docker:                              ## Clean Docker stuff
	$(dc) down

.PHONY: clean ## Remove all file artifacts
clean: clean-build clean-pyc clean-coverage clean-pytest clean-docs-build clean-docker
install:                            ## Install dev dependencies in local environment
	pip install --upgrade pip
	pip install -r requirements/local.txt

showmigrations:                     ## Show migrations
	$(manage) showmigrations

migrations:                         ## Make migrations with ARGS=appname
	$(manage) makemigrations $(ARGS)

migrate:                            ## Migrate
	$(manage) migrate

collectstatic:                      ## Collect static files
	$(manage) collectstatic --noinput

.PHONY: urls
urls:                               ## Show URL endpoints
	$(manage) show_urls

superuser:                          ## Create a superuser (user with admin rights)
	$(manage) createsuperuser

logs:                               ## Tail container logs
	$(dc) logs -f

run:                                ## Run Docker environment (reloads env vars)
	$(dc) up --build --remove-orphans -d

run-debug:                          ## Run Docker environment with attachable debugger
	DJANGO_DEBUG=True $(dc) up --build --remove-orphans -d

stop:                               ## Stop Docker environment
	$(dc) stop

restart:                            ## Restart Docker environment
	$(dc) restart

build:                              ## Build Docker images
	$(dc) build

build-no-cache:                     ## Build Docker image with ARGS="container_name"
	$(dc) build $(ARGS) --no-cache

status:                             ## Show container status
	$(dc) ps

bash:                               ## Run a terminal shell command with ARGS="some command"
	$(run) $(ARGS)

manage:                             ## Run a manage.py command with ARGS="some command"
	$(manage) $(ARGS)

shell:                              ## Run a Django IDE shell in the app container
	$(manage) shell

shell-plus:                         ## Run a Django IDE shell_plus in the app container
	$(manage) shell_plus

dbshell:                            ## Run a psql shell in the app container
	$(manage) dbshell

backup-db:                          ## Backup database
	$(dc) run --rm postgres /usr/local/bin/backup

restore-db:                         ## Restore database with ARGS="backup_file.sql.gz"
	$(dc) run --rm postgres /usr/local/bin/restore $(ARGS)

clearsessions:                      ## Clear database connections
	$(manage) clearsessions

.PHONY: test
test:                               ## Run fast backend unit tests
	$(pytest) -m "not slow"

test-all:                           ## Run all backend unit tests
	$(pytest)

# Run all unit tests but stop on first error and drop into pdf to debug
pdb:                                ## Run all unit tests
	$(pytest) -x --pdb

# Run all unit tests (report to terminal) with a coverage report
test-cov-term:     ## Run all unit tests with a report (terminal)
	$(pytest) --cov --cov-report term

test-cov-html:     ## Run all unit tests with a report (html)
	$(pytest) --cov --cov-report html

generate-secret:                    ## Generate a secret and print to terminal
	$(manage) shell -c "from django.core.management import utils; print(utils.get_random_secret_key())"
