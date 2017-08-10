#! /bin/bash

set -e

source ./venv/bin/activate || exit 1
pep8 --exclude=migrations datasubmission/
pep8 --exclude=migrations shared_server/
