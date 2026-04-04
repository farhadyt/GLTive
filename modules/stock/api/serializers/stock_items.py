# Purpose: Serializers for StockItem entity with separate create/update/output
"""
Stock Item Serializers
Enforces immutability of item_model_id, warehouse_id, tracking_type on update.
"""
from rest_framework import serializers

from modules.stock.models import StockItem


class StockItemCreateSerializer(serializers.Serializer):
    item_model_id = serializers.UUIDField()
    warehouse_id = serializers.UUIDField()
    internal_code = serializers.CharField(max_length=80, required=False, allow_blank=True, allow_null=True)
    item_name_override = serializers.CharField(max_length=180, required=False, allow_blank=True, allow_null=True)
    minimum_stock_level_override = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=False, allow_null=True
    )
    notes = serializers.CharField(required=False, allow_blank=True, default="")


class StockItemUpdateSerializer(serializers.Serializer):
    internal_code = serializers.CharField(max_length=80, required=False, allow_blank=True, allow_null=True)
    item_name_override = serializers.CharField(max_length=180, required=False, allow_blank=True, allow_null=True)
    minimum_stock_level_override = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=False, allow_null=True
    )
    notes = serializers.CharField(required=False, allow_blank=True)


class StockItemOutputSerializer(serializers.ModelSerializer):
    item_model_id = serializers.UUIDField(source="item_model.pk", read_only=True)
    warehouse_id = serializers.UUIDField(source="warehouse.pk", read_only=True)

    class Meta:
        model = StockItem
        fields = [
            "id",
            "item_model_id",
            "warehouse_id",
            "internal_code",
            "item_name_override",
            "tracking_type",
            "quantity_on_hand",
            "quantity_reserved",
            "quantity_available",
            "minimum_stock_level_override",
            "last_received_at",
            "last_issued_at",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = fields
