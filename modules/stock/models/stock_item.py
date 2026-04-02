from django.db import models
from core.models.base import CompanyScopedModel

class StockItem(CompanyScopedModel):
    """
    Central aggregated stock record for a given model in a specific warehouse.
    """
    item_model = models.ForeignKey(
        "stock.ItemModel",
        on_delete=models.RESTRICT,
        related_name="stock_items"
    )
    warehouse = models.ForeignKey(
        "stock.Warehouse",
        on_delete=models.RESTRICT,
        related_name="stock_items"
    )
    
    internal_code = models.CharField(max_length=80, null=True, blank=True, db_index=True)
    item_name_override = models.CharField(max_length=180, null=True, blank=True)
    
    tracking_type = models.CharField(max_length=30, db_index=True)
    
    quantity_on_hand = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    quantity_reserved = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    quantity_available = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    
    minimum_stock_level_override = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    
    last_received_at = models.DateTimeField(null=True, blank=True, db_index=True)
    last_issued_at = models.DateTimeField(null=True, blank=True, db_index=True)
    
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "stock_items"
        verbose_name = "Stock Item"
        verbose_name_plural = "Stock Items"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "warehouse", "item_model"],
                condition=models.Q(is_deleted=False),
                name="unique_active_stock_item_per_warehouse_per_company"
            ),
            models.UniqueConstraint(
                fields=["company", "internal_code"],
                condition=models.Q(is_deleted=False, internal_code__isnull=False),
                name="unique_active_internal_code_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company", "warehouse", "is_active", "is_deleted"]),
            models.Index(fields=["company", "item_model", "is_active", "is_deleted"]),
            models.Index(fields=["company", "tracking_type"]),
            models.Index(fields=["company", "quantity_available"]),
        ]

    def __str__(self):
        return f"{self.item_name_override or self.item_model.model_name} in {self.warehouse.code}"
