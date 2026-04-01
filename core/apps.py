# Purpose: Django app configuration for the core platform module
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Platform core: authentication, tenancy, permissions, base models."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Platform Core"
