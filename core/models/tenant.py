# Purpose: Tenant and Company models for multi-tenant row-level isolation
"""
GLTive Tenant / Company Models
Multi-tenant foundation with row-level isolation.
"""
from django.db import models

from core.models.base import BaseModel


class Tenant(BaseModel):
    """
    Represents a tenant in the platform (vendor-level grouping).
    A tenant can own multiple companies.

    TODO: Implement full tenant lifecycle:
    - Tenant onboarding flow
    - Tenant status management (active, suspended, terminated)
    - Tenant quota and entitlement linkage
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "tenants"
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self):
        return self.name


class Company(BaseModel):
    """
    Represents a customer company within a tenant.
    All business data is scoped to a Company.

    TODO: Implement full company management:
    - Company profile and settings
    - Working calendar
    - Internal admin model
    - Company dashboard
    """

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="companies",
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "companies"
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "code"],
                name="unique_company_code_per_tenant",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"
