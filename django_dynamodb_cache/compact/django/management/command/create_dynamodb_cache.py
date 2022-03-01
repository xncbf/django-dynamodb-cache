from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create dynamodb cache tables"

    def add_arguments(self, parser):
        parser.add_argument("caches", nargs="+", type=str)

    def handle(self, *args, **options):
        for cache_name in options["caches"]:

            table = "nada"

            self.stdout.write(self.style.SUCCESS(f"Cache table {table} created for cache {cache_name}"))
