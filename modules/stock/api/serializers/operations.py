# Purpose: Command serializers for stock receive, issue, and transfer operations
"""
Operation Command Serializers
Plain Serializer classes for validating command payloads — not ModelSerializers.
"""
from decimal import Decimal

from rest_framework import serializers


class ReceiveQuantitySerializer(serializers.Serializer):
    stock_item_id = serializers.UUIDField()
    quantity = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=Decimal("0.01"))
    unit_cost = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=False, allow_null=True, min_value=Decimal("0")
    )
    reference_type = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    reference_id = serializers.UUIDField(required=False, allow_null=True)
    reason_code = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    note = serializers.CharField(required=False, allow_blank=True, default="")


class ReceiveSerializedUnitSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=150)
    asset_tag_candidate = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    condition_status = serializers.ChoiceField(
        choices=["new", "good", "used", "damaged", "defective"],
        required=False,
        default="new",
    )
    note = serializers.CharField(required=False, allow_blank=True, default="")


class ReceiveSerializedSerializer(serializers.Serializer):
    stock_item_id = serializers.UUIDField()
    units = ReceiveSerializedUnitSerializer(many=True, min_length=1)
    unit_cost = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=False, allow_null=True, min_value=0
    )
    reference_type = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    reference_id = serializers.UUIDField(required=False, allow_null=True)
    reason_code = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    note = serializers.CharField(required=False, allow_blank=True, default="")


class IssueQuantitySerializer(serializers.Serializer):
    stock_item_id = serializers.UUIDField()
    quantity = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=Decimal("0.01"))
    reference_type = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    reference_id = serializers.UUIDField(required=False, allow_null=True)
    reason_code = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    note = serializers.CharField(required=False, allow_blank=True, default="")


class IssueSerializedSerializer(serializers.Serializer):
    stock_item_id = serializers.UUIDField()
    serial_unit_ids = serializers.ListField(child=serializers.UUIDField(), min_length=1)
    reference_type = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    reference_id = serializers.UUIDField(required=False, allow_null=True)
    reason_code = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    note = serializers.CharField(required=False, allow_blank=True, default="")


class TransferQuantitySerializer(serializers.Serializer):
    source_stock_item_id = serializers.UUIDField()
    target_warehouse_id = serializers.UUIDField()
    quantity = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=Decimal("0.01"))
    reason_code = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    note = serializers.CharField(required=False, allow_blank=True, default="")


class TransferSerializedSerializer(serializers.Serializer):
    source_stock_item_id = serializers.UUIDField()
    target_warehouse_id = serializers.UUIDField()
    serial_unit_ids = serializers.ListField(child=serializers.UUIDField(), min_length=1)
    reason_code = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    note = serializers.CharField(required=False, allow_blank=True, default="")
