# Purpose: Role and Permission models for minimal company-scoped RBAC
"""
GLTive Access Models
Provides the minimal DB-backed role and permission structures for platform access.
"""
from django.db import models
from core.models.base import BaseModel, CompanyScopedModel


class Permission(BaseModel):
    """
    Represents an explicit capability in the system.
    e.g., code = 'stock.view', name = 'View Stock'
    """

    code = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "permissions"
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self):
        return self.code


class Role(CompanyScopedModel):
    """
    Represents a group of permissions assigned to users within a specific company.
    """

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(
        Permission,
        related_name="roles",
        blank=True,
    )

    class Meta:
        db_table = "roles"
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_role_name_per_company",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.company.name})"
