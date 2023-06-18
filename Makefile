SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:

NAME := ankigpt
DOCKERFILE := ./Dockerfile
VERSION := latest
NETWORK := bridge
OPENAI_API_KEY := 
OPENAI_ORG := 

.PHONY: help
help:
	$(info Available make targets:)
	@egrep '^(.+)\:\ ##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'

.PHONY: build
build: ## Build docker image
	$(info *** Building docker image: $(NAME):$(VERSION))
	@docker build \
		--tag $(NAME):$(VERSION) \
		--file $(DOCKERFILE) \
		.

.PHONY: serve
serve: ## Launch the app
	$(info *** Launch the app)
	@ docker run --rm -d \
		--network=$(NETWORK) \
		--env OPENAI_API_KEY=$(OPENAI_API_KEY) \
		--env OPENAI_ORG=$(OPENAI_ORG) \
		--name=$(NAME) \
		-p 8501:8501 \
	  --volume ~/workdir/$(NAME):/workdir \
		$(NAME):$(VERSION)
