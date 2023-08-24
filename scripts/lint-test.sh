#!/usr/bin/env bash

set -x

poetry run black django_dynamodb_cache --check
poetry run ruff check --exit-zero .
