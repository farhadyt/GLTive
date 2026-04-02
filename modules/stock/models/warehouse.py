from django.db import models
from core.models.base import CompanyScopedModel, SoftDeleteModel

class Warehouse(CompanyScopedModel, SoftDeleteModel):
    """
    Physical warehouse or storage location anchor.
    """
    code = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=150, db_index=True)
    
    # location_reference_id = models.UUIDField(null=True, blank=True)  # Future capability
    
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "warehouses"
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                condition=models.Q(is_deleted=False),
                name="unique_active_warehouse_code_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company", "is_active", "is_deleted"]),
            models.Index(fields=["company", "is_default", "is_active", "is_deleted"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"
