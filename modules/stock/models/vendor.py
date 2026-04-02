from django.db import models
from core.models.base import CompanyScopedModel

class Vendor(CompanyScopedModel):
    """
    Vendor / supplier registry for procurement and stock references.
    """
    name = models.CharField(max_length=180, db_index=True)
    normalized_name = models.CharField(max_length=180, db_index=True)
    code = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    contact_person = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "vendor_references"
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "normalized_name"],
                condition=models.Q(is_deleted=False),
                name="unique_active_normalized_vendor_name_per_company"
            ),
            models.UniqueConstraint(
                fields=["company", "code"],
                condition=models.Q(is_deleted=False, code__isnull=False),
                name="unique_active_vendor_code_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company", "is_active", "is_deleted"]),
            models.Index(fields=["company", "normalized_name"]),
            models.Index(fields=["company", "code"]),
        ]

    def __str__(self):
        return self.name
