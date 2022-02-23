#!/usr/bin/env bash

set -x

poetry run black django_dynamodb_cache --check
poetry run isort --check-only django_dynamodb_cache
poetry run flake8
