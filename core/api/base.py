# Purpose: Base company-scoped API ViewSet for module reuse
"""
GLTive Base API Foundation
Provides a reusable viewset foundation to enforce safe cross-company boundary behavior.
"""
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from core.permissions.base import IsCompanyMember


class CompanyScopedViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet for any module that handles company-specific data.
    Automatically restricts all queries to the request's active company context.
    """
    permission_classes = [IsCompanyMember]

    def get_queryset(self):
        """
        Overrides the DRF default get_queryset to mandate filtering.
        We expect `self.queryset` to be defined on children, and we append `.filter(company=...)`.
        """
        # Ensure underlying implementation provided a queryset or model to work with
        assert getattr(self, "queryset", None) is not None, (
            f"'{self.__class__.__name__}' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method directly if doing something complex."
        )

        qs = self.queryset
        if hasattr(self.request, "company") and self.request.company:
            # Enforce the tenant boundary inherently
            return qs.filter(company=self.request.company)

        # Fallback denial (although IsCompanyMember generally prevents this state)
        return qs.none()

    def perform_create(self, serializer):
        """
        Automatically bind the company to newly created entities.
        Raises PermissionDenied if no company context is available — company-scoped
        records must never be created without an explicit company binding.
        """
        if hasattr(self.request, "company") and self.request.company:
            serializer.save(company=self.request.company)
        else:
            raise PermissionDenied(
                "Company context is required to create company-scoped resources."
            )
