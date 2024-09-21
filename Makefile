.PHONY: env install lint test freeze package build clean

.DEFAULT_GOAL := build

BUILDER=@python3 -m scripts.builder

env:
	$(BUILDER) create-env

install:
	pip3 install --upgrade pip
	pip3 install -r requirements-dev.txt

lint:
	$(BUILDER) run-lint

test:
	$(BUILDER) run-tests

freeze:
	$(BUILDER) freeze-deps

package:
	$(BUILDER) package-project

build:
	$(BUILDER) build-project

clean:
	$(BUILDER) clean-project
