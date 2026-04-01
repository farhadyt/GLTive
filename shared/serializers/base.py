# Purpose: Base serializer classes with standard audit field handling
"""
GLTive Base Serializers
Standard serializer patterns for the platform.
"""
from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer for all GLTive models.
    Automatically handles read-only audit fields.
    """

    class Meta:
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )


class CompanyScopedSerializer(BaseModelSerializer):
    """
    Serializer for company-scoped models.
    company is automatically set from request context, not from user input.
    """

    class Meta(BaseModelSerializer.Meta):
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ("company",)
