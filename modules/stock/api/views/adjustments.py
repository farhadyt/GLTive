# Purpose: APIViews for stock adjustment session lifecycle
"""
Adjustment Views
Create session, upsert lines, confirm, cancel.

Design decision:
    Alert evaluation after confirm is a post-operation follow-up, intentionally
    separated from the main confirm transaction. Alert evaluation failure does
    NOT invalidate an already successful adjustment confirmation. The confirm
    result is the primary response; alert evaluation is secondary.
"""
import logging

from rest_framework.permissions import IsAuthenticated

from core.api.base import CompanyScopedAPIView
from core.permissions.base import IsCompanyMember
from modules.stock.api.permissions import CanAdjustStock
from modules.stock.api.serializers.adjustments import (
    AdjustmentSessionCreateSerializer,
    AdjustmentSessionOutputSerializer,
    AdjustmentLinesUpsertSerializer,
    AdjustmentLineOutputSerializer,
)
from modules.stock.models import StockAdjustmentLine, StockItem
from modules.stock.services import StockAdjustmentService, StockAlertService
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


class CreateAdjustmentSessionView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanAdjustStock]

    def post(self, request):
        serializer = AdjustmentSessionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = StockAdjustmentService.create_adjustment_session(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = AdjustmentSessionOutputSerializer(session)
        return created_response(data=output.data)


class UpsertAdjustmentLinesView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanAdjustStock]

    def put(self, request, session_id):
        serializer = AdjustmentLinesUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lines = StockAdjustmentService.upsert_adjustment_lines(
            company=request.company,
            session_id=session_id,
            lines_data=serializer.validated_data["lines_data"],
            actor=request.user,
        )
        output = AdjustmentLineOutputSerializer(lines, many=True)
        return success_response(data=output.data)


class ConfirmAdjustmentSessionView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanAdjustStock]

    def post(self, request, session_id):
        result = StockAdjustmentService.confirm_adjustment_session(
            company=request.company,
            session_id=session_id,
            actor=request.user,
        )
        # Alert evaluation AFTER confirmation — company-scoped bulk fetch
        affected_item_ids = StockAdjustmentLine.objects.filter(
            adjustment_session_id=result["session_id"],
            company=request.company,
        ).values_list("stock_item_id", flat=True).distinct()

        affected_items = StockItem.objects.filter(
            pk__in=affected_item_ids,
            company=request.company,
        )
        for stock_item in affected_items:
            _safe_evaluate_alerts(request.company, stock_item)

        return success_response(data=result)


class CancelAdjustmentSessionView(CompanyScopedAPIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanAdjustStock]

    def post(self, request, session_id):
        session = StockAdjustmentService.cancel_adjustment_session(
            company=request.company,
            session_id=session_id,
            actor=request.user,
        )
        output = AdjustmentSessionOutputSerializer(session)
        return success_response(data=output.data)
