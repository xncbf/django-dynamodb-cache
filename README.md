# django-dynamodb-cache [WIP]

Serverless cache backend for Django

Working with: AWS Dynamodb

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
  - [Create cache table command](#create-cache-table-command)
  - [How to contribute](#how-to-contribute)

## Installation

```sh
pip install django-dynamodb-cache
```

## Setup on Django

On Django Settings

```python
    instaled_apps = [
        ...
        'django_dynamodb_cache.compact.django'
    ]

    CACHES = {
        'default': {
            'BACKEND': 'django_dynamodb_cache.compact.django.cache.DjangoCacheDynamodb',
            'TIMEOUT': 120  # default 120 seconds == 2minutes
            'KEY_PREFIX': 'django_dynamodb_cache'  # default django_dynamodb_cache
            'VERSION': 1  # default 1
            'KEY_FUNCTION': 'path.to.function' # f'{prefix}:{key}:{version}'

            'OPTIONS': {
                'aws_access_key_id': None       # need only if you dont have login
                'aws_secret_access_key': None   # on aws-cli with your key
                'aws_region_name': None         # or not in aws lambda

                'read_capacity_units': 1
                'write_capacity_units': 1
                'encode': 'path.to.encode'  # default: 'django_dynamodb_cache.encode.PickleEncode
            }
        }
    }
```

## Create cache table command

Run manage command to create cache table on Dynamodb before using

`python manage.py create_dynamodb_cache`

## How to contribute


**WIP**
