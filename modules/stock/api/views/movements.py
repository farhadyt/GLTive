# Purpose: Read-only ViewSet for stock movement history
"""
Movement History Views
Read-only. Queries StockMovement model directly — acceptable for read-only
endpoints with no business logic. This is a documented design decision,
not a service-layer violation.
"""
from django.db.models import Q

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.api.base import CompanyResolveMixin
from core.permissions.base import IsCompanyMember
from modules.stock.api.permissions import CanViewHistory
from modules.stock.api.serializers.movements import MovementOutputSerializer
from modules.stock.models import StockMovement


class MovementViewSet(CompanyResolveMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Read-only movement history endpoint.
    Design decision: queries StockMovement directly (no service layer needed
    for pure read-only, no-business-logic queries).
    """
    permission_classes = [IsAuthenticated, IsCompanyMember, CanViewHistory]
    serializer_class = MovementOutputSerializer

    def get_queryset(self):
        if not hasattr(self.request, "company") or self.request.company is None:
            return StockMovement.objects.none()

        qs = StockMovement.objects.filter(
            company=self.request.company,
        ).select_related(
            "stock_item",
            "stock_item__item_model",
            "source_warehouse",
            "target_warehouse",
            "performed_by",
        ).order_by("-performed_at")

        # Filterable by query params
        stock_item_id = self.request.query_params.get("stock_item_id")
        if stock_item_id:
            qs = qs.filter(stock_item_id=stock_item_id)

        warehouse_id = self.request.query_params.get("warehouse_id")
        if warehouse_id:
            qs = qs.filter(
                Q(source_warehouse_id=warehouse_id) | Q(target_warehouse_id=warehouse_id)
            )

        movement_type = self.request.query_params.get("movement_type")
        if movement_type:
            qs = qs.filter(movement_type=movement_type)

        date_from = self.request.query_params.get("date_from")
        if date_from:
            qs = qs.filter(performed_at__gte=date_from)

        date_to = self.request.query_params.get("date_to")
        if date_to:
            qs = qs.filter(performed_at__lte=date_to)

        return qs
