from django.db import models
from core.models.base import CompanyScopedModel

class StockAdjustmentSession(CompanyScopedModel):
    """
    Session for grouping stock counts and reconciliation.
    """
    STATUS_DRAFT = "draft"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    warehouse = models.ForeignKey(
        "stock.Warehouse",
        on_delete=models.RESTRICT,
        related_name="adjustment_sessions"
    )
    session_code = models.CharField(max_length=60, db_index=True)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT, db_index=True)
    
    confirmed_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="confirmed_adjustments"
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "stock_adjustment_sessions"
        verbose_name = "Adjustment Session"
        verbose_name_plural = "Adjustment Sessions"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "session_code"],
                name="unique_session_code_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company", "warehouse", "status"]),
            models.Index(fields=["company", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.session_code} - {self.status}"


class StockAdjustmentLine(CompanyScopedModel):
    """
    Line-level detail under an adjustment session.
    """
    adjustment_session = models.ForeignKey(
        StockAdjustmentSession,
        on_delete=models.CASCADE,
        related_name="lines"
    )
    stock_item = models.ForeignKey(
        "stock.StockItem",
        on_delete=models.RESTRICT,
        related_name="adjustment_lines"
    )
    expected_quantity = models.DecimalField(max_digits=14, decimal_places=2)
    counted_quantity = models.DecimalField(max_digits=14, decimal_places=2)
    difference_quantity = models.DecimalField(max_digits=14, decimal_places=2)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "stock_adjustment_lines"
        verbose_name = "Adjustment Line"
        verbose_name_plural = "Adjustment Lines"
        constraints = [
            models.UniqueConstraint(
                fields=["adjustment_session", "stock_item"],
                name="unique_item_per_adjustment_session"
            )
        ]
        indexes = [
            models.Index(fields=["company", "stock_item"]),
        ]

    def __str__(self):
        return f"{self.stock_item} diff {self.difference_quantity}"
