# Purpose: APIViews for stock adjustment session lifecycle
"""
Adjustment Views
Create session, upsert lines, confirm, cancel.
Alert evaluation triggered after confirm for all affected stock items.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

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


class CreateAdjustmentSessionView(APIView):
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


class UpsertAdjustmentLinesView(APIView):
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


class ConfirmAdjustmentSessionView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanAdjustStock]

    def post(self, request, session_id):
        result = StockAdjustmentService.confirm_adjustment_session(
            company=request.company,
            session_id=session_id,
            actor=request.user,
        )
        # Alert evaluation AFTER confirmation for all affected stock items
        lines = StockAdjustmentLine.objects.filter(
            adjustment_session_id=result["session_id"],
        )
        for line in lines:
            stock_item = StockItem.objects.get(pk=line.stock_item_id)
            StockAlertService.evaluate_alerts_for_stock_item(
                company=request.company, stock_item=stock_item,
            )
        return success_response(data=result)


class CancelAdjustmentSessionView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanAdjustStock]

    def post(self, request, session_id):
        session = StockAdjustmentService.cancel_adjustment_session(
            company=request.company,
            session_id=session_id,
            actor=request.user,
        )
        output = AdjustmentSessionOutputSerializer(session)
        return success_response(data=output.data)
