from django.db import models
from core.models.base import CompanyScopedModel
import uuid

class StockMovement(CompanyScopedModel):
    """
    Immutable stock movement history foundation.
    """
    TYPE_STOCK_IN = "stock_in"
    TYPE_STOCK_OUT = "stock_out"
    TYPE_TRANSFER_IN = "transfer_in"
    TYPE_TRANSFER_OUT = "transfer_out"
    TYPE_ADJUSTMENT_PLUS = "adjustment_plus"
    TYPE_ADJUSTMENT_MINUS = "adjustment_minus"
    TYPE_RESERVE = "reserve"
    TYPE_RELEASE_RESERVE = "release_reserve"

    TYPE_CHOICES = [
        (TYPE_STOCK_IN, "Stock In"),
        (TYPE_STOCK_OUT, "Stock Out"),
        (TYPE_TRANSFER_IN, "Transfer In"),
        (TYPE_TRANSFER_OUT, "Transfer Out"),
        (TYPE_ADJUSTMENT_PLUS, "Adjustment Plus"),
        (TYPE_ADJUSTMENT_MINUS, "Adjustment Minus"),
        (TYPE_RESERVE, "Reserve"),
        (TYPE_RELEASE_RESERVE, "Release Reserve"),
    ]

    movement_type = models.CharField(max_length=30, choices=TYPE_CHOICES, db_index=True)
    
    stock_item = models.ForeignKey(
        "stock.StockItem", 
        on_delete=models.RESTRICT, 
        related_name="movements"
    )
    stock_serial_unit = models.ForeignKey(
        "stock.StockSerialUnit",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="movements"
    )
    
    source_warehouse = models.ForeignKey(
        "stock.Warehouse",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="movements_out"
    )
    target_warehouse = models.ForeignKey(
        "stock.Warehouse",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="movements_in"
    )
    
    quantity = models.DecimalField(max_digits=14, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    
    reference_type = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    reference_id = models.UUIDField(null=True, blank=True, db_index=True)
    reason_code = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    note = models.TextField(blank=True)
    
    performed_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="performed_stock_movements"
    )
    performed_at = models.DateTimeField(db_index=True)

    class Meta:
        db_table = "stock_movements"
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"
        indexes = [
            models.Index(fields=["company", "stock_item", "-performed_at"]),
            models.Index(fields=["company", "movement_type", "-performed_at"]),
            models.Index(fields=["company", "source_warehouse", "-performed_at"]),
            models.Index(fields=["company", "target_warehouse", "-performed_at"]),
        ]

    def __str__(self):
        return f"{self.movement_type} for {self.stock_item_id} at {self.performed_at}"

    def save(self, *args, **kwargs):
        """
        Enforce immutability. Existing movements cannot be changed.
        """
        if not self._state.adding:
            raise ValueError("StockMovement records are immutable and cannot be updated.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Enforce immutability. Movements cannot be deleted.
        """
        raise ValueError("StockMovement records are immutable and cannot be deleted.")
