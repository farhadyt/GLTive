# Purpose: Read-only serializer for stock movement history
"""
Movement Serializers
Read-only output with stock item summary, warehouse names, performed_by username.
"""
from rest_framework import serializers

from modules.stock.models import StockMovement


class MovementOutputSerializer(serializers.ModelSerializer):
    stock_item_id = serializers.UUIDField(source="stock_item.pk", read_only=True)
    stock_item_name = serializers.SerializerMethodField()
    source_warehouse_name = serializers.SerializerMethodField()
    target_warehouse_name = serializers.SerializerMethodField()
    performed_by_username = serializers.SerializerMethodField()

    class Meta:
        model = StockMovement
        fields = [
            "id",
            "movement_type",
            "stock_item_id",
            "stock_item_name",
            "quantity",
            "unit_cost",
            "source_warehouse_name",
            "target_warehouse_name",
            "reference_type",
            "reference_id",
            "reason_code",
            "note",
            "performed_by_username",
            "performed_at",
            "created_at",
        ]
        read_only_fields = fields

    def get_stock_item_name(self, obj):
        return obj.stock_item.item_name_override or obj.stock_item.item_model.model_name

    def get_source_warehouse_name(self, obj):
        return obj.source_warehouse.name if obj.source_warehouse else None

    def get_target_warehouse_name(self, obj):
        return obj.target_warehouse.name if obj.target_warehouse else None

    def get_performed_by_username(self, obj):
        return obj.performed_by.username if obj.performed_by else None
