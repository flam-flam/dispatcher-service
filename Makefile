.DEFAULT_GOAL := help
include .env
export

build: ## Build the image with a dev tag
	@docker build -t dispatcher:dev .

run: build ## Run the dispatcher with the default config
	@docker run -it --env-file .env -v `pwd`/config.json:/src/config.json dispatcher:dev

dependencies: ## Install pip depencencies
	@echo "..... Installing depencencies"
	@pip install -r tests/requirements.txt --quiet

lint: dependencies ## Fun flake8 linter
	@echo "..... Linting"
	@python -m flake8

test: dependencies ## Run pytest
	@echo "..... Running tests"
	@python -m pytest && $(MAKE) lint


.PHONY: help
help: ## Display this help
	@echo "\nUsage:\n  make \033[36m<target>\033[0m"
	@awk 'BEGIN {FS = ":.*##"}; \
		/^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } \
		/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } \
		/^###@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } \
		/^###&/ { printf "\t\t  \033[33m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
