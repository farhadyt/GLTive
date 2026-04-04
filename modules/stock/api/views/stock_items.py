# Purpose: CRUD ViewSet for StockItem with service-layer write pattern
"""
Stock Item ViewSet
Separate create/update serializers. tracking_type, item_model_id, warehouse_id immutable on update.
"""
from rest_framework.decorators import action

from core.api.base import CompanyScopedViewSet
from modules.stock.api.permissions import CanManageStock, CanViewStock
from modules.stock.api.serializers.stock_items import (
    StockItemCreateSerializer,
    StockItemUpdateSerializer,
    StockItemOutputSerializer,
)
from modules.stock.models import StockItem
from modules.stock.services import StockItemService
from shared.responses.base import success_response, created_response


class StockItemViewSet(CompanyScopedViewSet):
    queryset = StockItem.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_deleted=False)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [CanViewStock()]
        return [CanManageStock()]

    def get_serializer_class(self):
        if self.action == "create":
            return StockItemCreateSerializer
        if self.action in ("update", "partial_update"):
            return StockItemUpdateSerializer
        return StockItemOutputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockItemService.create_stock_item(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = StockItemOutputSerializer(result)
        return created_response(data=output.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=kwargs.get("partial", False))
        serializer.is_valid(raise_exception=True)
        result = StockItemService.update_stock_item(
            company=request.company,
            stock_item_id=instance.pk,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = StockItemOutputSerializer(result)
        return success_response(data=output.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        instance = self.get_object()
        result = StockItemService.deactivate_stock_item(
            company=request.company,
            stock_item_id=instance.pk,
            actor=request.user,
        )
        output = StockItemOutputSerializer(result)
        return success_response(data=output.data)
