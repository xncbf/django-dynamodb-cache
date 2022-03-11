import os
import shutil
import sys
from unittest import TestCase

import django
from django.core.management import call_command

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.django.settings"

# Set up Django
django.setup()


class TestDjangoApp(TestCase):
    def test_command(self):
        shutil.rmtree("tests/migrations", True)
        call_command("makemigrations", "tests", verbosity=2 if "-v" in sys.argv else 0)
