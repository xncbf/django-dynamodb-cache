from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create dynamodb cache tables"

    def add_arguments(self, parser):
        parser.add_argument("caches", nargs="+", type=str)

    def handle(self, *args, **options):
        from django.conf import Settings, settings

        from django_dynamodb_cache.dynamodb import get_dynamodb

        # Because settings are imported lazily, we need to explicitly load them.
        if not settings.configured:
            settings._setup()

        settings = Settings()
        dynamodb = get_dynamodb(settings)
        self.create_table(settings, dynamodb)

    def create_table(self, settings, database):
        from django_dynamodb_cache.dynamodb import create_table

        create_table(settings, database)
        # BaseDatabaseCache(settings.tablename)
        table = "nada"
        cachename = "TODO: option's cache name"
        self.stdout.write(self.style.SUCCESS(f"Cache table {table} created for cache {cachename}"))
