# Purpose: Immutable audit log model mechanism
"""
GLTive Audit Model
Guarantees the persistence of immutable audit events globally.
"""
from django.db import models
from core.models.base import BaseModel


class AuditLog(BaseModel):
    """
    Immutable ledger of system activity.
    Once written, an AuditLog can never be updated or deleted.
    """

    actor_user = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    company = models.ForeignKey(
        "core.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    action_code = models.CharField(max_length=200, db_index=True)
    target_entity_type = models.CharField(max_length=150)
    target_entity_id = models.CharField(max_length=150)

    before_snapshot = models.JSONField(null=True, blank=True)
    after_snapshot = models.JSONField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "audit_logs"
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action_code} on {self.target_entity_type}:{self.target_entity_id}"

    def save(self, *args, **kwargs):
        """
        Enforce immutability. Block updates.
        """
        if not self._state.adding:
            raise ValueError("AuditLogs are immutable and cannot be modified.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Enforce immutability. Block deletions.
        """
        raise ValueError("AuditLogs are immutable and cannot be deleted.")
