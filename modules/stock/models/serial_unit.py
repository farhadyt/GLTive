from django.db import models
from core.models.base import CompanyScopedModel

class StockSerialUnit(CompanyScopedModel):
    """
    Individual serialized units for serial-tracked inventory.
    """
    STATUS_IN_STOCK = "in_stock"
    STATUS_RESERVED = "reserved"
    STATUS_ISSUED = "issued"
    STATUS_DAMAGED = "damaged"
    STATUS_RETIRED = "retired"

    STATUS_CHOICES = [
        (STATUS_IN_STOCK, "In Stock"),
        (STATUS_RESERVED, "Reserved"),
        (STATUS_ISSUED, "Issued"),
        (STATUS_DAMAGED, "Damaged"),
        (STATUS_RETIRED, "Retired"),
    ]

    CONDITION_NEW = "new"
    CONDITION_GOOD = "good"
    CONDITION_USED = "used"
    CONDITION_DAMAGED = "damaged"
    CONDITION_DEFECTIVE = "defective"

    CONDITION_CHOICES = [
        (CONDITION_NEW, "New"),
        (CONDITION_GOOD, "Good"),
        (CONDITION_USED, "Used"),
        (CONDITION_DAMAGED, "Damaged"),
        (CONDITION_DEFECTIVE, "Defective"),
    ]

    stock_item = models.ForeignKey(
        "stock.StockItem",
        on_delete=models.RESTRICT,
        related_name="serial_units"
    )
    warehouse = models.ForeignKey(
        "stock.Warehouse",
        on_delete=models.RESTRICT,
        related_name="serial_units"
    )
    
    serial_number = models.CharField(max_length=150, db_index=True)
    asset_tag_candidate = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    
    condition_status = models.CharField(max_length=30, choices=CONDITION_CHOICES, default=CONDITION_NEW)
    stock_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_IN_STOCK, db_index=True)
    
    received_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "stock_serial_units"
        verbose_name = "Stock Serial Unit"
        verbose_name_plural = "Stock Serial Units"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "serial_number"],
                condition=models.Q(is_deleted=False),
                name="unique_active_serial_number_per_company"
            ),
            models.UniqueConstraint(
                fields=["company", "asset_tag_candidate"],
                condition=models.Q(is_deleted=False, asset_tag_candidate__isnull=False),
                name="unique_active_asset_tag_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company", "stock_item", "stock_status", "is_deleted"]),
            models.Index(fields=["company", "warehouse", "stock_status", "is_deleted"]),
            models.Index(fields=["company", "serial_number"]),
        ]

    def __str__(self):
        return f"{self.serial_number} - {self.stock_status}"
