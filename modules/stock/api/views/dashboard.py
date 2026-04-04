# Purpose: Read-only APIViews for stock dashboard metrics
"""
Dashboard Views
All read-only. Call StockDashboardService methods, return plain dicts in success_response.
"""
from rest_framework.permissions import IsAuthenticated

from core.api.base import CompanyScopedAPIView
from core.permissions.base import IsCompanyMember
from modules.stock.api.permissions import CanViewStock
from modules.stock.services import StockDashboardService
from shared.responses.base import success_response


class DashboardSummaryView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanViewStock]

    def get(self, request):
        data = StockDashboardService.get_summary(company=request.company)
        return success_response(data=data)


class DashboardRecentMovementsView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanViewStock]

    def get(self, request):
        limit = request.query_params.get("limit", 10)
        try:
            limit = min(int(limit), 50)
        except (ValueError, TypeError):
            limit = 10
        data = StockDashboardService.get_recent_movements(
            company=request.company, limit=limit,
        )
        return success_response(data=data)


class DashboardLowStockView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanViewStock]

    def get(self, request):
        limit = request.query_params.get("limit", 20)
        try:
            limit = min(int(limit), 50)
        except (ValueError, TypeError):
            limit = 20
        data = StockDashboardService.get_low_stock_items(
            company=request.company, limit=limit,
        )
        return success_response(data=data)
