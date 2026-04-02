# Purpose: Custom User model with company association for tenant-aware auth
"""
GLTive Custom User Model
Extends Django AbstractUser with company linkage.
"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for GLTive platform.
    Links users to a company for tenant-scoped access.

    # Phase 1 Minimal Access additions:
    # ---------------------------------
    # is_platform_admin: Master vendor admin marker (can transcend companies).
    # is_company_admin: Company-level admin bypass mapping.
    # role: Minimal role-to-permission mapping for standard users.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    company = models.ForeignKey(
        "core.Company",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users",
    )
    role = models.ForeignKey(
        "core.Role",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    
    # Access and routing flags
    is_platform_admin = models.BooleanField(
        default=False, 
        help_text="Designates whether the user is a vendor-level administrative user."
    )
    is_company_admin = models.BooleanField(
        default=False,
        help_text="Designates whether the user acts as an admin for their associated company."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
