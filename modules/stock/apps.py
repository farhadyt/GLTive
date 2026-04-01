# Purpose: Django app configuration for the Stock/Inventory Foundation module
from django.apps import AppConfig


class StockConfig(AppConfig):
    """Module 01: Stock / Inventory Foundation."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.stock"
    label = "stock"
    verbose_name = "Stock / Inventory Foundation"
