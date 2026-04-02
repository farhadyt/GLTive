from django.db import models
from core.models.base import CompanyScopedModel, SoftDeleteModel

class ItemModel(CompanyScopedModel, SoftDeleteModel):
    """
    Standard model/template definition of an item type.
    """
    TRACKING_QUANTITY = "quantity_based"
    TRACKING_SERIALIZED = "serialized"
    TRACKING_CHOICES = [
        (TRACKING_QUANTITY, "Quantity Based"),
        (TRACKING_SERIALIZED, "Serialized"),
    ]

    category = models.ForeignKey(
        "stock.StockCategory",
        on_delete=models.RESTRICT,
        related_name="item_models"
    )
    brand = models.ForeignKey(
        "stock.Brand",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="item_models"
    )
    vendor_reference = models.ForeignKey(
        "stock.Vendor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="item_models"
    )
    
    model_name = models.CharField(max_length=180)
    model_code = models.CharField(max_length=80, null=True, blank=True, db_index=True)
    normalized_model_name = models.CharField(max_length=180, db_index=True)
    description = models.TextField(blank=True)
    
    default_unit = models.CharField(max_length=30, default="pcs")
    tracking_type = models.CharField(
        max_length=30, 
        choices=TRACKING_CHOICES,
        db_index=True
    )
    minimum_stock_level = models.DecimalField(
        max_digits=14, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    image_url = models.URLField(max_length=500, blank=True)
    
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "item_models"
        verbose_name = "Item Model"
        verbose_name_plural = "Item Models"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "category", "normalized_model_name", "brand"],
                condition=models.Q(is_deleted=False),
                name="unique_active_item_model_identity_per_company"
            ),
            models.UniqueConstraint(
                fields=["company", "model_code"],
                condition=models.Q(is_deleted=False, model_code__isnull=False),
                name="unique_active_model_code_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company", "category", "is_active", "is_deleted"]),
            models.Index(fields=["company", "tracking_type", "is_active", "is_deleted"]),
        ]

    def __str__(self):
        return self.model_name
