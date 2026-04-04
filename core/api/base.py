# Purpose: Base company-scoped API ViewSet and APIView for module reuse
"""
GLTive Base API Foundation
Provides a reusable viewset and view foundation to enforce safe cross-company boundary behavior.

Architecture note:
    TenantMiddleware sets request.company during Django's middleware phase, which
    works for session-based auth. However, with JWT authentication, the user is not
    authenticated until DRF's view dispatch (perform_authentication). CompanyResolveMixin
    bridges this gap by resolving request.company after DRF authentication completes,
    ensuring company context is available before permission checks run.
"""
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from core.permissions.base import IsCompanyMember


class CompanyResolveMixin:
    """
    Resolves request.company after DRF authentication.
    Must be placed before APIView/ViewSet in MRO so super() chains correctly.
    """

    def perform_authentication(self, request):
        super().perform_authentication(request)
        if not getattr(request, "company", None):
            if request.user and request.user.is_authenticated:
                company = getattr(request.user, "company", None)
                if company:
                    request.company = company


class CompanyScopedViewSet(CompanyResolveMixin, viewsets.ModelViewSet):
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
        assert getattr(self, "queryset", None) is not None, (
            f"'{self.__class__.__name__}' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method directly if doing something complex."
        )

        qs = self.queryset
        if hasattr(self.request, "company") and self.request.company:
            return qs.filter(company=self.request.company)

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


class CompanyScopedAPIView(CompanyResolveMixin, APIView):
    """
    Base APIView for company-scoped command endpoints.
    Resolves request.company after JWT authentication, before permission checks.
    """
    pass
