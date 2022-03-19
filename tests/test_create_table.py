from unittest import TestCase

from moto import mock_dynamodb

from django_dynamodb_cache.dynamodb import create_table, get_dynamodb
from django_dynamodb_cache.settings import Settings
from tests.conf import TABLE_NAME


@mock_dynamodb
class TestCreateTable(TestCase):
    def test_create_table_simple(self):
        settings = Settings(aws_region_name="us-east-1", table_name=TABLE_NAME)
        dynamodb = get_dynamodb(settings)
        table = create_table(settings, dynamodb)
        self.assertEqual(table.table_name, TABLE_NAME)
        self.assertEqual(table.table_status, "ACTIVE")
