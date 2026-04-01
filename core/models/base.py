# Purpose: Base model mixins providing UUID PK, timestamps, soft-delete, and company scoping
"""
GLTive Base Models
Foundational abstract models that all platform entities inherit from.
"""
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract base model for all GLTive entities.
    Provides UUID primary key and timestamp tracking.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class AuditableModel(BaseModel):
    """
    Extends BaseModel with user tracking for create/update operations.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )

    class Meta:
        abstract = True


class SoftDeleteModel(AuditableModel):
    """
    Extends AuditableModel with soft-delete capability.
    Records are never hard-deleted; they are flagged as deleted.
    """

    is_active = models.BooleanField(default=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_deleted",
    )

    class Meta:
        abstract = True

    def soft_delete(self, user=None):
        """Mark this record as deleted without removing it from the database."""
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save(update_fields=["is_deleted", "is_active", "deleted_at", "deleted_by", "updated_at"])

    def restore(self):
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.is_active = True
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=["is_deleted", "is_active", "deleted_at", "deleted_by", "updated_at"])


class CompanyScopedModel(SoftDeleteModel):
    """
    Extends SoftDeleteModel with company (tenant) isolation.
    All company-scoped business entities must inherit from this model.
    """

    company = models.ForeignKey(
        "core.Company",
        on_delete=models.CASCADE,
        related_name="%(class)s_set",
        db_index=True,
    )

    class Meta:
        abstract = True
