# Purpose: Serializers for stock master data entities (Category, Brand, Vendor, ItemModel, Warehouse)
"""
Master Data Serializers
CRUD serializers for stock master data with explicit field control.
"""
from rest_framework import serializers

from modules.stock.models import (
    StockCategory,
    Brand,
    Vendor,
    ItemModel,
    Warehouse,
)


class CategorySerializer(serializers.ModelSerializer):
    parent_category_id = serializers.UUIDField(required=False, allow_null=True)

    class Meta:
        model = StockCategory
        fields = [
            "id",
            "code",
            "name",
            "description",
            "parent_category_id",
            "sort_order",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "description",
            "website",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "id",
            "name",
            "code",
            "contact_person",
            "email",
            "phone",
            "address",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class ItemModelCreateSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    brand_id = serializers.UUIDField(required=False, allow_null=True)
    vendor_reference_id = serializers.UUIDField(required=False, allow_null=True)
    model_name = serializers.CharField(max_length=180)
    model_code = serializers.CharField(max_length=80, required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    default_unit = serializers.CharField(max_length=30, required=False, default="pcs")
    tracking_type = serializers.ChoiceField(choices=ItemModel.TRACKING_CHOICES)
    minimum_stock_level = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=False, allow_null=True
    )
    image_url = serializers.URLField(max_length=500, required=False, allow_blank=True, default="")


class ItemModelUpdateSerializer(serializers.Serializer):
    category_id = serializers.UUIDField(required=False)
    brand_id = serializers.UUIDField(required=False, allow_null=True)
    vendor_reference_id = serializers.UUIDField(required=False, allow_null=True)
    model_name = serializers.CharField(max_length=180, required=False)
    model_code = serializers.CharField(max_length=80, required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    default_unit = serializers.CharField(max_length=30, required=False)
    minimum_stock_level = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=False, allow_null=True
    )
    image_url = serializers.URLField(max_length=500, required=False, allow_blank=True)


class ItemModelOutputSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(source="category.pk", read_only=True)
    brand_id = serializers.UUIDField(source="brand.pk", read_only=True, allow_null=True)
    vendor_reference_id = serializers.UUIDField(source="vendor_reference.pk", read_only=True, allow_null=True)

    class Meta:
        model = ItemModel
        fields = [
            "id",
            "category_id",
            "brand_id",
            "vendor_reference_id",
            "model_name",
            "model_code",
            "description",
            "default_unit",
            "tracking_type",
            "minimum_stock_level",
            "image_url",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = fields


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            "id",
            "code",
            "name",
            "location_reference_id",
            "description",
            "is_default",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "id",
            "is_default",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
