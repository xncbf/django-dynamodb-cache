from unittest.mock import patch

import boto3
import pytest


@pytest.fixture(autouse=True)
def mocked_dynamodb():
    with patch("django_dynamodb_cache.dynamodb.get_dynamodb", return_value=""):
        session = boto3.session.Session()
        dynamodb = session.resource("dynamodb", region_name="us-east-1", endpoint_url="http://localhost:8000")
        yield dynamodb
