from django.db import models
from core.models.base import CompanyScopedModel, SoftDeleteModel

class Brand(CompanyScopedModel, SoftDeleteModel):
    """
    Brand or manufacturer registry for stock references.
    """
    name = models.CharField(max_length=150, db_index=True)
    normalized_name = models.CharField(max_length=150, db_index=True)
    description = models.TextField(blank=True)
    website = models.URLField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "brands"
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "normalized_name"],
                condition=models.Q(is_deleted=False),
                name="unique_active_normalized_brand_name_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company", "is_active", "is_deleted"]),
        ]

    def __str__(self):
        return self.name
