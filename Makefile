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
	pylint layers/ lambda_functions/ tests/ scripts/ setup.py

test:
	pytest tests/

package:
	$(BUILDER) package-project

build: clean
	$(BUILDER) deps
	$(BUILDER) pack --delete-staging-after layers/common
	$(BUILDER) pack --delete-staging-after lambda_functions/get_clubs_by_organization
	$(BUILDER) pack --delete-staging-after lambda_functions/get_countries
	$(BUILDER) pack --delete-staging-after lambda_functions/get_match_records
	$(BUILDER) pack --delete-staging-after lambda_functions/get_organizations
	$(BUILDER) pack --delete-staging-after lambda_functions/get_states

clean:
	rm -f *.zip
	rm -rf dependencies/

