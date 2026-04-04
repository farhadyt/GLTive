# Purpose: Serializers for stock adjustment sessions and lines
"""
Adjustment Serializers
Handles adjustment session creation, line upsert, and output formatting.
"""
from decimal import Decimal

from rest_framework import serializers

from modules.stock.models import StockAdjustmentSession, StockAdjustmentLine


class AdjustmentSessionCreateSerializer(serializers.Serializer):
    warehouse_id = serializers.UUIDField()
    reason = serializers.CharField(required=False, allow_blank=True, default="")


class AdjustmentLineInputSerializer(serializers.Serializer):
    stock_item_id = serializers.UUIDField()
    counted_quantity = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=Decimal("0"))
    note = serializers.CharField(required=False, allow_blank=True, default="")


class AdjustmentLinesUpsertSerializer(serializers.Serializer):
    lines_data = AdjustmentLineInputSerializer(many=True, min_length=1)


class AdjustmentLineOutputSerializer(serializers.ModelSerializer):
    stock_item_id = serializers.UUIDField(source="stock_item.pk", read_only=True)

    class Meta:
        model = StockAdjustmentLine
        fields = [
            "id",
            "stock_item_id",
            "expected_quantity",
            "counted_quantity",
            "difference_quantity",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class AdjustmentSessionOutputSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.UUIDField(source="warehouse.pk", read_only=True)
    lines = AdjustmentLineOutputSerializer(many=True, read_only=True)

    class Meta:
        model = StockAdjustmentSession
        fields = [
            "id",
            "session_code",
            "warehouse_id",
            "reason",
            "status",
            "created_by",
            "confirmed_by",
            "confirmed_at",
            "created_at",
            "updated_at",
            "lines",
        ]
        read_only_fields = fields
