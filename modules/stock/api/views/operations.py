# Purpose: Command APIViews for stock receive, issue, and transfer operations
"""
Operation Command Views
Each is a separate APIView with post(). Alert evaluation called AFTER service operation.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

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


class ReceiveQuantityView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanReceiveStock]

    def post(self, request):
        serializer = ReceiveQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockReceiveService.receive_quantity_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        # Alert evaluation AFTER transaction commits
        stock_item = StockItem.objects.get(pk=result["stock_item_id"])
        StockAlertService.evaluate_alerts_for_stock_item(
            company=request.company, stock_item=stock_item,
        )
        return created_response(data=result)


class ReceiveSerializedView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanReceiveStock]

    def post(self, request):
        serializer = ReceiveSerializedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockReceiveService.receive_serialized_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        stock_item = StockItem.objects.get(pk=result["stock_item_id"])
        StockAlertService.evaluate_alerts_for_stock_item(
            company=request.company, stock_item=stock_item,
        )
        return created_response(data=result)


class IssueQuantityView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanIssueStock]

    def post(self, request):
        serializer = IssueQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockIssueService.issue_quantity_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        stock_item = StockItem.objects.get(pk=result["stock_item_id"])
        StockAlertService.evaluate_alerts_for_stock_item(
            company=request.company, stock_item=stock_item,
        )
        return success_response(data=result)


class IssueSerializedView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanIssueStock]

    def post(self, request):
        serializer = IssueSerializedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockIssueService.issue_serialized_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        stock_item = StockItem.objects.get(pk=result["stock_item_id"])
        StockAlertService.evaluate_alerts_for_stock_item(
            company=request.company, stock_item=stock_item,
        )
        return success_response(data=result)


class TransferQuantityView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanTransferStock]

    def post(self, request):
        serializer = TransferQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockTransferService.transfer_quantity_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        # Evaluate alerts for BOTH source and target
        source = StockItem.objects.get(pk=result["source_stock_item_id"])
        target = StockItem.objects.get(pk=result["target_stock_item_id"])
        StockAlertService.evaluate_alerts_for_stock_item(
            company=request.company, stock_item=source,
        )
        StockAlertService.evaluate_alerts_for_stock_item(
            company=request.company, stock_item=target,
        )
        return success_response(data=result)


class TransferSerializedView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyMember, CanTransferStock]

    def post(self, request):
        serializer = TransferSerializedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = StockTransferService.transfer_serialized_stock(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        source = StockItem.objects.get(pk=result["source_stock_item_id"])
        target = StockItem.objects.get(pk=result["target_stock_item_id"])
        StockAlertService.evaluate_alerts_for_stock_item(
            company=request.company, stock_item=source,
        )
        StockAlertService.evaluate_alerts_for_stock_item(
            company=request.company, stock_item=target,
        )
        return success_response(data=result)
