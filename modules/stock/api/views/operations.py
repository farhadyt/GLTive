# Purpose: Command APIViews for stock receive, issue, and transfer operations
"""
Operation Command Views
Each is a separate APIView with post(). Alert evaluation called AFTER service operation.

Design decision:
    Alert evaluation is a post-operation follow-up, intentionally separated from
    the main mutation transaction. Alert evaluation failure does NOT invalidate
    an already successful stock mutation response. This is by design — the stock
    mutation is the primary operation; alert evaluation is secondary.
"""
import logging

from rest_framework.permissions import IsAuthenticated

from core.api.base import CompanyScopedAPIView
from core.permissions.base import IsCompanyMember
from modules.stock.api.permissions import (
    CanReceiveStock,
    CanIssueStock,
    CanTransferStock,
)
from modules.stock.api.serializers.operations import (
    ReceiveQuantitySerializer,
    ReceiveSerializedSerializer,
    IssueQuantitySerializer,
    IssueSerializedSerializer,
    TransferQuantitySerializer,
    TransferSerializedSerializer,
)
from modules.stock.models import StockItem
from modules.stock.services import (
    StockReceiveService,
    StockIssueService,
    StockTransferService,
    StockAlertService,
)
from shared.responses.base import success_response, created_response

logger = logging.getLogger(__name__)


def _safe_evaluate_alerts(company, stock_item):
    """
    Evaluate alerts for a stock item in a failure-safe manner.
    If alert evaluation raises any exception, it is logged but does NOT
    propagate — the main stock operation response remains unaffected.
    """
    try:
        StockAlertService.evaluate_alerts_for_stock_item(
            company=company, stock_item=stock_item,
        )
    except Exception:
        logger.exception(
            "Alert evaluation failed for stock_item=%s company=%s — "
            "main operation succeeded, alert follow-up suppressed.",
            stock_item.pk, company.pk,
        )


class ReceiveQuantityView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanReceiveStock]

    def post(self, request):
        serializer = ReceiveQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockReceiveService.receive_quantity_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        # Alert evaluation AFTER transaction commits — company-scoped fetch
        stock_item = StockItem.objects.get(
            pk=result["stock_item_id"], company=request.company,
        )
        _safe_evaluate_alerts(request.company, stock_item)
        return created_response(data=result)


class ReceiveSerializedView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanReceiveStock]

    def post(self, request):
        serializer = ReceiveSerializedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockReceiveService.receive_serialized_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        stock_item = StockItem.objects.get(
            pk=result["stock_item_id"], company=request.company,
        )
        _safe_evaluate_alerts(request.company, stock_item)
        return created_response(data=result)


class IssueQuantityView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanIssueStock]

    def post(self, request):
        serializer = IssueQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockIssueService.issue_quantity_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        stock_item = StockItem.objects.get(
            pk=result["stock_item_id"], company=request.company,
        )
        _safe_evaluate_alerts(request.company, stock_item)
        return success_response(data=result)


class IssueSerializedView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanIssueStock]

    def post(self, request):
        serializer = IssueSerializedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockIssueService.issue_serialized_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        stock_item = StockItem.objects.get(
            pk=result["stock_item_id"], company=request.company,
        )
        _safe_evaluate_alerts(request.company, stock_item)
        return success_response(data=result)


class TransferQuantityView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanTransferStock]

    def post(self, request):
        serializer = TransferQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockTransferService.transfer_quantity_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        # Evaluate alerts for BOTH source and target — company-scoped
        source = StockItem.objects.get(
            pk=result["source_stock_item_id"], company=request.company,
        )
        target = StockItem.objects.get(
            pk=result["target_stock_item_id"], company=request.company,
        )
        _safe_evaluate_alerts(request.company, source)
        _safe_evaluate_alerts(request.company, target)
        return success_response(data=result)


class TransferSerializedView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanTransferStock]

    def post(self, request):
        serializer = TransferSerializedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockTransferService.transfer_serialized_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        source = StockItem.objects.get(
            pk=result["source_stock_item_id"], company=request.company,
        )
        target = StockItem.objects.get(
            pk=result["target_stock_item_id"], company=request.company,
        )
        _safe_evaluate_alerts(request.company, source)
        _safe_evaluate_alerts(request.company, target)
        return success_response(data=result)
