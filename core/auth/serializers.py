# Purpose: Custom JWT authentication serializers including company scope
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends the standard simplejwt obtain pair to include company
    context and platform admin indicators directly inside the generic payload.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["company_id"] = str(user.company.id) if user.company else None
        token["is_platform_admin"] = user.is_platform_admin
        token["is_company_admin"] = user.is_company_admin

        return token


class LogoutSerializer(serializers.Serializer):
    """
    Validates refresh token payload for blacklisting.
    """
    refresh = serializers.CharField(required=True)
