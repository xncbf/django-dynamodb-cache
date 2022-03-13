from django.conf import settings
from django.core.cache import caches
from django.core.management.base import BaseCommand

from django_dynamodb_cache.backend import DjangoCacheBackend
from django_dynamodb_cache.dynamodb import create_table


class Command(BaseCommand):
    help = "Creates the tables needed to use the DynamoDB cache backend."

    requires_system_checks = []

    def handle(self, *tablenames, **options):
        for cache_alias in settings.CACHES:
            cache = caches[cache_alias]
            if isinstance(cache, DjangoCacheBackend):
                self.create_table(cache_alias, cache._table)

    def create_table(self, cache_alias, tablename):
        from django_dynamodb_cache.backend import DjangoCacheBackend

        backend = DjangoCacheBackend(tablename, settings.CACHES[cache_alias])
        _settings = backend.settings
        dynamodb = backend.dynamodb
        # dynamodb = get_dynamodb(settings)
        table = create_table(_settings, dynamodb)
        self.stdout.write(self.style.SUCCESS(f"Cache table {table.table_arn} created for cache {cache_alias}"))
