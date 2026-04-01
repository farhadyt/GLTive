# Purpose: Marks config as a Python package and initializes Celery app
try:
    from config.celery import app as celery_app

    __all__ = ["celery_app"]
except ImportError:
    # Celery is optional during basic Django management commands
    # (e.g., migrate, check) when async infrastructure is unavailable.
    pass
