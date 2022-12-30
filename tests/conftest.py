import pytest

from django_dynamodb_cache import Cache
from django_dynamodb_cache.dynamodb import create_table, get_dynamodb
from django_dynamodb_cache.settings import Settings

from .conf import TABLE_NAME


@pytest.fixture(scope="session")
def cache():
    settings = Settings(aws_region_name="us-east-1", table_name=TABLE_NAME)
    dynamodb = get_dynamodb(settings)
    cache = Cache(settings)
    table = create_table(settings, dynamodb)
    yield cache
    print("teardown")
    table.delete(
        TableName=settings.table_name,
    )
