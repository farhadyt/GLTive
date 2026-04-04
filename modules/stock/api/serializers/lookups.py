# Purpose: Lightweight lookup serializers for UI dropdowns
"""
Lookup Serializers
Minimal id + display field(s) only. No audit fields, no descriptions, no nested objects.
"""
from rest_framework import serializers

from modules.stock.models import (
    StockCategory,
    Brand,
    Vendor,
    Warehouse,
    ItemModel,
    StockItem,
)


class CategoryLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockCategory
        fields = ["id", "code", "name"]
        read_only_fields = fields


class BrandLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]
        read_only_fields = fields


class VendorLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "code"]
        read_only_fields = fields


class WarehouseLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "code", "name"]
        read_only_fields = fields


class ItemModelLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = ["id", "model_name", "model_code", "tracking_type"]
        read_only_fields = fields


class StockItemLookupSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = StockItem
        fields = ["id", "display_name", "internal_code", "tracking_type"]
        read_only_fields = fields

    def get_display_name(self, obj):
        return obj.item_name_override or obj.item_model.model_name
