# Purpose: Stock module permission classes for granular endpoint access control
"""
Stock Permissions
Thin DRF permission wrappers around stock permission codes.
"""
from rest_framework.permissions import BasePermission


def make_stock_permission(perm_code):
    """Factory that creates a DRF permission class for a stock permission code."""

    class StockPermission(BasePermission):
        def has_permission(self, request, view):
            if not request.user or not request.user.is_authenticated:
                return False

            if getattr(request.user, "is_platform_admin", False):
                return True

            if not hasattr(request, "company") or request.company is None:
                return False

            if getattr(request.user, "is_company_admin", False):
                return True

            role = getattr(request.user, "role", None)
            if not role:
                return False

            return role.permissions.filter(code=perm_code).exists()

    StockPermission.__name__ = f"Has_{perm_code.replace('.', '_')}"
    StockPermission.__qualname__ = StockPermission.__name__
    return StockPermission


CanViewStock = make_stock_permission("stock.view")
CanManageStock = make_stock_permission("stock.manage")
CanManageMasterData = make_stock_permission("stock.master.manage")
CanReceiveStock = make_stock_permission("stock.receive")
CanIssueStock = make_stock_permission("stock.issue")
CanTransferStock = make_stock_permission("stock.transfer")
CanAdjustStock = make_stock_permission("stock.adjust")
CanManageAlerts = make_stock_permission("stock.alert.manage")
CanViewHistory = make_stock_permission("stock.history.view")
