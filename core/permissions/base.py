# Purpose: Base permission classes for company-scoped API access control
"""
GLTive Base Permissions
Real role and tenant permission foundation classes mapping to the access model.
"""
from rest_framework.permissions import BasePermission


class IsCompanyMember(BasePermission):
    """
    User must belong to a company scope safely.
    Platform admins implicitly pass if they are manipulating global scopes, but
    for standard business endpoints, request.company presence is required.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Optional bypass for platform admins
        if getattr(request.user, "is_platform_admin", False):
            return True
            
        return hasattr(request, "company") and request.company is not None


class IsCompanyAdmin(BasePermission):
    """
    User must have company-admin privileges.
    """

    def has_permission(self, request, view):
        if not IsCompanyMember().has_permission(request, view):
            return False

        # Platform admins implicitly hold company admin power everywhere
        if getattr(request.user, "is_platform_admin", False):
            return True

        return getattr(request.user, "is_company_admin", False)


class HasModulePermission(BasePermission):
    """
    Extensible module permission checking.
    Usage:
        permission_classes = [HasModulePermission("stock.view")]
    """
    def __init__(self, required_permission=None):
        self.required_permission = required_permission

    def __call__(self):
        return self

    def has_permission(self, request, view):
        # Allow views to define a static required_permission attribute
        perm_code = self.required_permission or getattr(view, "required_permission", None)
        
        if not perm_code:
            return False

        if not IsCompanyMember().has_permission(request, view):
            return False

        # Vendor/Platform admin bypass
        if getattr(request.user, "is_platform_admin", False):
            return True

        # Check DB-backed roles
        user = request.user
        if not getattr(user, "role", None):
            return False

        # Avoid N+1 issues by evaluating through minimal subquery/fetching if needed,
        # but locally hitting cached relationships is standard for DRF
        return user.role.permissions.filter(code=perm_code).exists()
