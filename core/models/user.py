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

    TODO: Implement full user lifecycle:
    - Role and permission engine integration
    - Employee profile linkage
    - Session policy enforcement
    - MFA support
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
