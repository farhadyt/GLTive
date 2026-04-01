# Purpose: Base permission classes for company-scoped API access control
"""
GLTive Base Permissions
Foundation permission classes for the platform's role-based access control.

TODO: Implement:
- IsCompanyMember — user belongs to the target company
- IsCompanyAdmin — user has admin role within their company
- IsPlatformAdmin — vendor-level platform admin
- HasModulePermission — user has specific module permission (e.g., stock.view)
- Permission guard decorators for service layer
"""
from rest_framework.permissions import BasePermission


class IsCompanyMember(BasePermission):
    """
    Allows access only to users who belong to a company.

    TODO: Implement company membership check against request.user.company
    """

    def has_permission(self, request, view):
        # WARNING: This is a placeholder only — does NOT check company membership yet
        # TODO: Replace with actual company scope check before production use
        return request.user and request.user.is_authenticated
