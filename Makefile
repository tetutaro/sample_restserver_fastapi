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
	@rm -rf .mypy_cache/
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

.PHONY: req-health
req-health:
	curl -S -s -X GET -H "Content-Type: application/json" "localhost:8930/health"
	@echo "\n  === It should be SUCCESS ==="

.PHONY: req-version
req-version:
	curl -S -s -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/version"
	@echo "\n  === It should be SUCCESS ==="

.PHONY: req-wsgi-server
req-wsgi-server:
	curl -S -s -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/wsgi_server"
	@echo "\n  === It should be SUCCESS ==="

.PHONY: req-insert-number
req-insert-number:
	curl -S -s -X POST -H "Content-Type: application/json" "localhost:8930/api/v1/number" -d '{"item_id":"1234","number":5}'
	@echo "\n  === It should be SUCCESS ==="

.PHONY: req-insert-number-invalid-id
req-insert-number-invalid-id:
	curl -S -s -X POST -H "Content-Type: application/json" "localhost:8930/api/v1/number" -d '{"item_id":"123456","number":5}'
	@echo "\n  === It should be FAILED ==="

.PHONY: req-insert-number-invalid-val
req-insert-number-invalid-val:
	curl -S -s -X POST -H "Content-Type: application/json" "localhost:8930/api/v1/number" -d '{"item_id":"1234","number":100}'
	@echo "\n  === It should be FAILED ==="

.PHONY: req-insert-number-found
req-insert-number-found:
	curl -S -s -X POST -H "Content-Type: application/json" "localhost:8930/api/v1/number" -d '{"item_id":"12ab","number":3}'
	@echo "\n  === It should be FAILED ==="

.PHONY: req-insert-text
req-insert-text:
	curl -S -s -X POST -H "Content-Type: application/json" "localhost:8930/api/v1/text" -d '{"item_id":"abcd","text":"efgh"}'
	@echo "\n  === It should be SUCCESS ==="

.PHONY: req-insert-text-invalid-id
req-insert-text-invalid-id:
	curl -S -s -X POST -H "Content-Type: application/json" "localhost:8930/api/v1/text" -d '{"item_id":"abcdehff","text":"efgh"}'
	@echo "\n  === It should be FAILED ==="

.PHONY: req-insert-text-invalid-val
req-insert-text-invalid-val:
	curl -S -s -X POST -H "Content-Type: application/json" "localhost:8930/api/v1/text" -d '{"item_id":"abcd","text":"efghxxxxxxxxxxxxxxxxx"}'
	@echo "\n  === It should be FAILED ==="

.PHONY: req-insert-text-found
req-insert-text-found:
	curl -S -s -X POST -H "Content-Type: application/json" "localhost:8930/api/v1/text" -d '{"item_id":"ab34","text":"ijkl"}'
	@echo "\n  === It should be FAILED ==="

.PHONY: req-delete
req-delete:
	curl -S -s -X DELETE -H "Content-Type: application/json" "localhost:8930/api/v1/delete/ab12"
	@echo "  === It should be SUCCESS ==="

.PHONY: req-delete-notfound
req-delete-notfound:
	curl -S -s -X DELETE -H "Content-Type: application/json" "localhost:8930/api/v1/delete/ab1234ie"
	@echo "\n  === It should be FAILED ==="

.PHONY: req-ref-number
req-ref-number:
	curl -S -s -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/number/1234"
	@echo "\n  === It should be SUCCESS ==="

.PHONY: req-ref-number-notfound
req-ref-number-notfound:
	curl -S -s -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/number/12cd"
	@echo "\n  === It should be FAILED ==="

.PHONY: req-ref-text
req-ref-text:
	curl -S -s -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/text/abcd"
	@echo "\n  === It should be SUCCESS ==="

.PHONY: req-ref-text-notfound
req-ref-text-notfound:
	curl -S -s -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/text/ab34"
	@echo "\n  === It should be FAILED ==="

.PHONY: req-count
req-count:
	curl -S -s -X GET -H "Content-Type: application/json" "localhost:8930/api/v1/count"
	@echo "\n  === It should be SUCCESS ==="

.PHONY: req-all
req-all: req-health req-version req-wsgi-server req-insert-number req-insert-number-invalid-id req-insert-number-invalid-val req-insert-number-found req-insert-text req-insert-text-invalid-id req-insert-text-invalid-val req-insert-text-found req-delete req-delete-notfound req-ref-number req-ref-number-notfound req-ref-text req-ref-text-notfound req-count
