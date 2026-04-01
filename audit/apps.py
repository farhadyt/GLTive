# Purpose: Django app configuration for the audit trail engine
from django.apps import AppConfig


class AuditConfig(AppConfig):
    """Immutable audit trail engine for all platform state changes."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "audit"
    verbose_name = "Audit Trail"
