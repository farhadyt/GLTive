# Purpose: APIViews for stock alert event list, acknowledge, and resolve
"""
Alert Views
Company-scoped alert event list and status transition endpoints.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.permissions.base import IsCompanyMember
from modules.stock.api.permissions import CanManageAlerts, CanViewStock
from modules.stock.api.serializers.alerts import AlertEventOutputSerializer
from modules.stock.models import StockAlertEvent
from modules.stock.services import StockAlertService
from shared.responses.base import success_response


class AlertListView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanViewStock]

    def get(self, request):
        queryset = StockAlertEvent.objects.filter(
            company=request.company,
        ).select_related("stock_item", "alert_rule").order_by("-created_at")

        # Optional status filter
        status_filter = request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        serializer = AlertEventOutputSerializer(queryset[:100], many=True)
        return success_response(data=serializer.data)


class AcknowledgeAlertView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanManageAlerts]

    def post(self, request, alert_id):
        event = StockAlertService.acknowledge_alert(
            company=request.company,
            alert_event_id=alert_id,
            actor=request.user,
        )
        output = AlertEventOutputSerializer(event)
        return success_response(data=output.data)


class ResolveAlertView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanManageAlerts]

    def post(self, request, alert_id):
        event = StockAlertService.resolve_alert(
            company=request.company,
            alert_event_id=alert_id,
            actor=request.user,
        )
        output = AlertEventOutputSerializer(event)
        return success_response(data=output.data)
