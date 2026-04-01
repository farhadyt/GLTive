# Purpose: Marks config as a Python package and initializes Celery app
import sys

# Skip Celery initialization for purely local/schema management commands 
# to ensure they don't fail if async infrastructure is unavailable.
__all__ = []
_skip_cmds = {"makemigrations", "migrate", "showmigrations", "check"}
if not _skip_cmds.intersection(sys.argv):
    try:
        from config.celery import app as celery_app
        __all__ = ["celery_app"]
    except ImportError:
        pass
