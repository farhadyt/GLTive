# Purpose: Serializers for stock alert events
"""
Alert Serializers
Read-only output serializer for stock alert events.
"""
from rest_framework import serializers

from modules.stock.models import StockAlertEvent


class AlertEventOutputSerializer(serializers.ModelSerializer):
    stock_item_id = serializers.UUIDField(source="stock_item.pk", read_only=True)
    alert_rule_id = serializers.UUIDField(source="alert_rule.pk", read_only=True, allow_null=True)

    class Meta:
        model = StockAlertEvent
        fields = [
            "id",
            "stock_item_id",
            "alert_rule_id",
            "alert_type",
            "triggered_value",
            "threshold_value",
            "status",
            "acknowledged_by",
            "acknowledged_at",
            "resolved_by",
            "resolved_at",
            "created_at",
        ]
        read_only_fields = fields
