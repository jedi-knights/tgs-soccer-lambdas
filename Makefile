.PHONY: install lint test freeze package clean

.DEFAULT_GOAL := build

env:
	python3 -m venv .venv

install:
	pip3 install --upgrade pip
	pip3 install -r requirements.txt

lint:
	pylint

test:
	pytest

freeze:
	pip3 freeze > requirements.txt

package:
	# Install dependencies
	if [ ! -d "dependencies" ]; then \
	 pip3 install -r requirements.txt -t dependencies/ > /dev/null 2>&1; \
	fi

	# package common lambda layer
	cp -r dependencies/* common/ > /dev/null 2>&1
	cd common/
	zip -r ../common_layer.zip . > /dev/null 2>&1
	cd ..

	# package lambda functions
	for dir in lambda_functions/*/; do \
	 cp -r dependencies/* $$dir > /dev/null 2>&1; \
	 cd $$dir; \
	 zip -r ../../$$(basename $$dir).zip . > /dev/null 2>&1; \
	 cd - > /dev/null 2>&1; \
	done

build: clean install lint test

clean:
	@rm -f *.zip
	@rm -rf dependencies/
	@find . -type d -name "packaging" -exec rm -rf {} +

	@find . -type d -name "*.dist-info" | while read -r dist_info_dir; do \
  	 package_dir=$$(dirname "$$dist_info_dir")/$$(basename "$$dist_info_dir" .dist-info); \
  	 rm -rf "$$dist_info_dir" "$$package_dir"; \
	done

	@for dir in _pytest bin boto3 botocore bs4 certifi charset_normalizer dateutil idna iniconfig jmespath pluggy pytest requests s3transfer soupsieve urllib3; do \
	  find . -type d -name "$$dir" ! -path "./venv/*" ! -path "./.venv/*" -exec rm -rf {} +; \
	done

	@for file in pipe.py py.py README.rst six.py; do \
	  find . -type f -name "$$file" ! -path "./venv/*" ! -path "./.venv/*" -exec rm -f {} +; \
	done
