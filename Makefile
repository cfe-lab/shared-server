PYTHON_SRC=$(find . \( -type d -path '*/venv' -prune \) -o -name '*.py')

SHELL=/bin/bash
VBIN=./venv/bin

usage:
	@echo "Targets: venv test check clean"

clean:
	rm -f to_webroot venv

venv: requirements.txt test-requirements.txt
	python3 -m venv venv
	${VBIN}/pip install -r requirements.txt -r test-requirements.txt
	touch venv  # update time on venv dir

test: dev_keys
	. dev_keys && ${VBIN}/python manage.py test

check: test
	${VBIN}/pycodestyle shared_server
	${VBIN}/flake8 shared_server

dev_keys: make_dev_keys.py
	python make_dev_keys.py > dev_keys
