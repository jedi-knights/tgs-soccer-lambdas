.PHONY: env install lint test freeze package build clean

.DEFAULT_GOAL := build

BUILDER=@python3 -m scripts.builder

env:
	rm -rf .venv
	python3 -m venv .venv

install:
	pip3 install --upgrade pip
	pip3 install -r requirements-dev.txt

uninstall:
	pip3 uninstall -r requirements.txt -y
	pip3 uninstall -r requirements-dev.txt -y

lint:
	pylint layer/ lambda_functions/ tests/ scripts/ setup.py

test:
	pytest tests/

package:
	$(BUILDER) package-project

build:
	$(BUILDER) build-project

clean:
	rm -f *.zip
	rm -rf dependencies/
	$(BUILDER) clean-project
