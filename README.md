# django-dynamodb-cache [WIP]

Fast, safe, cost-effective DynamoDB cache backend for Django

<p align="center">
<a href="https://codecov.io/gh/xncbf/django-dynamodb-cache" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/xncbf/django-dynamodb-cache?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/django-dynamodb-cache" target="_blank">
    <img src="https://img.shields.io/pypi/v/django-dynamodb-cache?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/django-dynamodb-cache" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/django-dynamodb-cache.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="http://pypi.python.org/pypi/django-dynamodb-cache" target="_blank">
    <img src="https://img.shields.io/badge/django-3.2-brightgreen.svg" alt="Coverage">
</a>
</p>

- [django-dynamodb-cache [WIP]](#django-dynamodb-cache-wip)
  - [Installation](#installation)
  - [Setup on Django](#setup-on-django)
  - [Aws credentials](#aws-credentials)
  - [Create cache table command](#create-cache-table-command)
  - [How to contribute](#how-to-contribute)

## Installation

```sh
pip install django-dynamodb-cache
```

## Setup on Django

On Django `settings.py`

```python


INSTALLED_APPS = [
    ...
    "django_dynamodb_cache"
]

CACHES = {
    "default": {
        "BACKEND": "django_dynamodb_cache.backend.DjangoCacheBackend",
        "TIMEOUT": 120,  # seconds
        "KEY_PREFIX": "django_dynamodb_cache",
        "VERSION": 1,
        "KEY_FUNCTION": "path.to.function",  # f"{prefix}:{key}:{version}"
        "OPTIONS": {
            "aws_region_name": "us-east-1",
            "read_capacity_units": 1,
            "write_capacity_units": 1,
            "encode": "django_dynamodb_cache.encode.PickleEncode"
        }
    }
}
```

## Aws credentials

The same method as configuring-credentials provided in the boto3 documentation is used.
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials

## Create cache table command

Run manage command to create cache table on Dynamodb before using

```zsh
python manage.py createcachetable
```

## How to contribute

**WIP**
