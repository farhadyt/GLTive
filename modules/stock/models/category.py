from django.db import models
from core.models.base import CompanyScopedModel

class StockCategory(CompanyScopedModel):
    """
    Classification for stock items.
    """
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="subcategories",
    )
    code = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=150, db_index=True)
    description = models.TextField(blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        db_table = "stock_item_categories"
        verbose_name = "Stock Category"
        verbose_name_plural = "Stock Categories"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                condition=models.Q(is_deleted=False),
                name="unique_active_category_code_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company", "is_active", "is_deleted"]),
            models.Index(fields=["company", "parent_category"]),
            models.Index(fields=["company", "name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"
