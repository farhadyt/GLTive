# Purpose: Idempotent bootstrap for stock module permission codes
"""
Bootstrap Stock Permissions
Creates the stock module permission records if they do not already exist.
Safe to run multiple times — uses get_or_create for idempotency.
"""
from django.core.management.base import BaseCommand

from core.models import Permission


STOCK_PERMISSIONS = [
    {
        "code": "stock.view",
        "name": "View Stock",
        "description": "View stock items, lookups, dashboard, and read-only data.",
    },
    {
        "code": "stock.manage",
        "name": "Manage Stock Items",
        "description": "Create, update, and deactivate stock item records.",
    },
    {
        "code": "stock.master.manage",
        "name": "Manage Stock Master Data",
        "description": "Manage categories, brands, vendors, item models, and warehouses.",
    },
    {
        "code": "stock.receive",
        "name": "Receive Stock",
        "description": "Receive quantity-based and serialized stock into inventory.",
    },
    {
        "code": "stock.issue",
        "name": "Issue Stock",
        "description": "Issue quantity-based and serialized stock from inventory.",
    },
    {
        "code": "stock.transfer",
        "name": "Transfer Stock",
        "description": "Transfer stock between warehouses.",
    },
    {
        "code": "stock.adjust",
        "name": "Adjust Stock",
        "description": "Create, manage, and confirm stock adjustment sessions.",
    },
    {
        "code": "stock.alert.manage",
        "name": "Manage Stock Alerts",
        "description": "Acknowledge and resolve stock alert events.",
    },
    {
        "code": "stock.history.view",
        "name": "View Stock Movement History",
        "description": "View immutable stock movement history logs.",
    },
]


class Command(BaseCommand):
    help = "Bootstrap stock module permission codes into the database (idempotent)."

    def handle(self, *args, **options):
        created_count = 0
        existing_count = 0

        for perm_data in STOCK_PERMISSIONS:
            _, created = Permission.objects.get_or_create(
                code=perm_data["code"],
                defaults={
                    "name": perm_data["name"],
                    "description": perm_data["description"],
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  Created: {perm_data['code']}"))
            else:
                existing_count += 1
                self.stdout.write(f"  Exists:  {perm_data['code']}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nStock permissions bootstrap complete: "
                f"{created_count} created, {existing_count} already existed."
            )
        )
