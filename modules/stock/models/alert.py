from django.db import models
from core.models.base import CompanyScopedModel

class StockAlertRule(CompanyScopedModel):
    """
    Defines threshold/alert policies.
    """
    RULE_MINIMUM_STOCK = "minimum_stock"

    RULE_CHOICES = [
        (RULE_MINIMUM_STOCK, "Minimum Stock"),
    ]

    stock_item = models.ForeignKey(
        "stock.StockItem",
        on_delete=models.CASCADE,
        related_name="alert_rules"
    )
    rule_type = models.CharField(max_length=30, choices=RULE_CHOICES, db_index=True)
    threshold_value = models.DecimalField(max_digits=14, decimal_places=2)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "stock_alert_rules"
        verbose_name = "Stock Alert Rule"
        verbose_name_plural = "Stock Alert Rules"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "stock_item", "rule_type"],
                condition=models.Q(is_active=True),
                name="unique_active_alert_rule_per_item_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company", "rule_type", "is_active"]),
            models.Index(fields=["company", "stock_item", "is_active"]),
        ]

    def __str__(self):
        return f"{self.rule_type} on {self.stock_item}"


class StockAlertEvent(CompanyScopedModel):
    """
    Stores alert trigger history/event record.
    """
    STATUS_OPEN = "open"
    STATUS_ACKNOWLEDGED = "acknowledged"
    STATUS_RESOLVED = "resolved"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_ACKNOWLEDGED, "Acknowledged"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    stock_item = models.ForeignKey(
        "stock.StockItem",
        on_delete=models.CASCADE,
        related_name="alert_events"
    )
    alert_rule = models.ForeignKey(
        StockAlertRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alert_events"
    )
    
    alert_type = models.CharField(max_length=30, db_index=True)
    triggered_value = models.DecimalField(max_digits=14, decimal_places=2)
    threshold_value = models.DecimalField(max_digits=14, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN, db_index=True)
    
    acknowledged_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acknowledged_stock_alerts"
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    resolved_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_stock_alerts"
    )
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "stock_alert_events"
        verbose_name = "Stock Alert Event"
        verbose_name_plural = "Stock Alert Events"
        indexes = [
            models.Index(fields=["company", "status", "-created_at"]),
            models.Index(fields=["company", "stock_item", "status"]),
            models.Index(fields=["company", "alert_type", "status"]),
        ]

    def __str__(self):
        return f"{self.alert_type} for {self.stock_item} ({self.status})"
