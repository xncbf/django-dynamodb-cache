import os
import shutil
from unittest import TestCase

import django
from django.core.management import call_command

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings.settings"

# Set up Django
django.setup()


class TestDjangoApp(TestCase):
    def test_command(self):
        shutil.rmtree("tests/migrations", True)
        call_command("createcachetable")
