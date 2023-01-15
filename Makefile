PACKAGE="sample-restserver-fastapi"

.PHONY: clean
clean: clean-python clean-package clean-tests clean-system

.PHONY: clean-python
clean-python:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*.pyd' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-package
clean-package:
	@rm -rf dist/
	@rm -rf build/
	@rm -rf .eggs/
	@find . -name '*.egg-info' -exec rm -rf {} +
	@find . -name '*.egg' -exec rm -rf {} +

.PHONY: clean-tests
clean-tests:
	@rm -rf .pytest_cache/
	@rm -rf .tox/
	@rm -f .coverage
	@rm -rf htmlcov/

.PHONY: clean-system
clean-system:
	@find . -name '*~' -exec rm -f {} +
	@find . -name '.DS_Store' -exec rm -f {} +

.PHONY: requirements
requirements:
	poetry export --without-hashes -f requirements.txt -o requirements.txt

.PHONY: build-package
build-package:
	$(eval VERSION := $(shell poetry version -s))
	poetry build
	@tar zxf dist/$(PACKAGE)-$(VERSION).tar.gz -C ./dist
	@cp dist/$(PACKAGE)-$(VERSION)/setup.py setup.py
	@black setup.py
	@rm -rf dist

.PHONY: install
install:
	python setup.py install

.PHONY: uninstall
uninstall:
	pip uninstall -y $(PACKAGE)

.PHONY: docs
docs:
	cd docs && make html

.PHONY: tests
tests: tests-python

.PHONY: tests-python
tests-python:
	poetry run pflake8 .
	poetry run pytest

.PHONY: tests-report
tests-report:
	python -u -m pytest -v --cov --cov-report=html

# add new version number.
# do this after committing changes to the local repositry
# and before pushing changes to the remote repository.
.PHONY: version-up
version-up:
ifdef VERSION
	git tag $(VERSION)
	poetry dynamic-versioning
	git add pyproject.toml backend/__init__.py
	git commit -m "$(VERSION)"
	git tag -f $(VERSION)
	git push
	git push --tags
else
	@echo "Usage: make version-up VERSION=vX.X.X"
endif

.PHONY: app
app:
	python -m app

.PHONY: req_health
req_health:
	curl -S -s -i -X GET -H "Content-Type: application/json" "localhost:8930/health"

.PHONY: req_version
req_version:
	curl -S -s -i -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/version"

.PHONY: req_wsgi_server
req_wsgi_server:
	curl -S -s -i -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/wsgi_server"

.PHONY: req_insert_number
req_insert_number:
	curl -S -s -i -X POST -H "Content-Type: application/json" "localhost:8930/api/v1/number" -d '{"item_id":"1234","number":5}'

.PHONY: req_insert_text
req_insert_text:
	curl -S -s -i -X POST -H "Content-Type: application/json" "localhost:8930/api/v1/text" -d '{"item_id":"abcd","text":"efgh"}'

.PHONY: req_delete
req_delete:
	curl -S -s -i -X DELETE -H "Content-Type: application/json" "localhost:8930/api/v1/delete/ab12"

.PHONY: req_ref_number
req_ref_number:
	curl -S -s -i -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/number/1234"

.PHONY: req_ref_text
req_ref_text:
	curl -S -s -i -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/text/abcd"

.PHONY: req_count
req_count:
	curl -S -s -i -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/count"
