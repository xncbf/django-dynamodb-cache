# django-dynamodb-cache

Fast, safe, cost-effective DynamoDB cache backend for Django

<p align="center">
<a href="https://github.com/xncbf/django-dynamodb-cache/actions/workflows/tests.yml" target="_blank">
    <img src="https://github.com/xncbf/django-dynamodb-cache/actions/workflows/tests.yml/badge.svg" alt="Tests">
</a>
<a href="https://codecov.io/gh/xncbf/django-dynamodb-cache" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/xncbf/django-dynamodb-cache?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/django-dynamodb-cache" target="_blank">
    <img src="https://img.shields.io/pypi/v/django-dynamodb-cache?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/django-dynamodb-cache" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/django-dynamodb-cache.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://pypi.org/project/django-dynamodb-cache" target="_blank">
    <img src="https://img.shields.io/pypi/djversions/django-dynamodb-cache.svg" alt="Supported django versions">
</a>
<a href="http://pypi.python.org/pypi/django-dynamodb-cache/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/xncbf/django-dynamodb-cache?color=gr" alt="License">
</a>
</p>

- [django-dynamodb-cache](#django-dynamodb-cache)
  - [Introduce](#introduce)
  - [Why should I use this?](#why-should-i-use-this)
  - [Installation](#installation)
  - [Setup on Django](#setup-on-django)
  - [Aws credentials](#aws-credentials)
  - [Create cache table command](#create-cache-table-command)
  - [How to contribute](#how-to-contribute)

## Introduce

This project is a cache backend using aws dynamodb.

This is compatible with the django official cache framework.

Did you set the boto3 permission?

Enter the django official command createcachetable and get started easily.

## Why should I use this?

- There are few management points, because dynamodb is a fully managed service.
- Data is safely stored unlike inmemory db.
- Because you only pay for what you use, it saves money on light projects such as side projects or back offices.
- If you use it in a side project and the speed slows down due to increased usage, you can easily switch to DAX.

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
        "LOCATION": "table-name",                  # (mandatory)
        "TIMEOUT": 120,                            # (optional) seconds
        "KEY_PREFIX": "django_dynamodb_cache",     # (optional)
        "VERSION": 1,                              # (optional)
        "KEY_FUNCTION": "path.to.function",        # (optional) f"{prefix}:{key}:{version}"
        "OPTIONS": {
            "aws_region_name": "us-east-1",                    # (optional)
            "aws_access_key_id": "aws_access_key_id",          # (optional)
            "aws_secret_access_key": "aws_secret_access_key",  # (optional)
            "is_on_demand": False,                 # (optional) default: True
            "read_capacity_units": 1,              # (optional)
            "write_capacity_units": 1,             # (optional)
            "encode": "django_dynamodb_cache.encode.PickleEncode"  # (optional)
        }
    }
}
```

## Aws credentials

The same method as configuring-credentials provided in the boto3 documentation is used.
<https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials>

## Create cache table command

Run manage command to create cache table on Dynamodb before using

```zsh
python manage.py createcachetable
```

## How to contribute

This project is welcome to contributions!

Please submit an issue ticket before submitting a patch.

Pull requests are merged into the main branch and should always remain available.

After passing all test code, it is reviewed and merged.
