from importlib import import_module
from logging import getLogger

try:
    import django
except ImportError:
    django = None

try:
    import werkzeug
except ImportError:
    werkzeug = None

logger = getLogger("django_dynamodb_cache")


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.

    Copy from django
    """

    if "." not in dotted_path:
        return import_module(dotted_path)

    module_path, class_name = dotted_path.rsplit(".", 1)
    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (module_path, class_name)) from err
