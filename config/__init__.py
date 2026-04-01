# Purpose: Marks config as a Python package and initializes Celery app
from config.celery import app as celery_app

__all__ = ["celery_app"]
