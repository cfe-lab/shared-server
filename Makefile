PYTHON_SRC=$(find . \( -type d -path '*/venv' -prune \) -o -name '*.py')

SHELL=/bin/bash
VBIN=./venv/bin

usage:
	@echo "Targets: venv test check clean"

clean:
	rm -rf to_webroot venv

venv: requirements.txt test-requirements.txt
	python3.6 -m venv venv  # Pin version for Django compatibility
	${VBIN}/pip install --upgrade pip
	${VBIN}/pip install -r requirements.txt -r test-requirements.txt
	touch venv  # update time on venv dir

test: dev_keys venv
	. dev_keys && ${VBIN}/python manage.py test

check: test
	${VBIN}/pycodestyle shared_server
	${VBIN}/flake8 shared_server

dev_keys: make_dev_keys.py venv
	${VBIN}/python make_dev_keys.py > dev_keys
