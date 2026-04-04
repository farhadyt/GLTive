# Purpose: Stock module URL routing — all endpoints under /api/v1/stock/
"""
Stock API URL Configuration
Registers all stock module endpoints with clean REST structure.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from modules.stock.api.views import (
    # Master data
    CategoryViewSet,
    BrandViewSet,
    VendorViewSet,
    ItemModelViewSet,
    WarehouseViewSet,
    # Stock items
    StockItemViewSet,
    # Operations
    ReceiveQuantityView,
    ReceiveSerializedView,
    IssueQuantityView,
    IssueSerializedView,
    TransferQuantityView,
    TransferSerializedView,
    # Adjustments
    CreateAdjustmentSessionView,
    UpsertAdjustmentLinesView,
    ConfirmAdjustmentSessionView,
    CancelAdjustmentSessionView,
    # Alerts
    AlertListView,
    AcknowledgeAlertView,
    ResolveAlertView,
    # Dashboard
    DashboardSummaryView,
    DashboardRecentMovementsView,
    DashboardLowStockView,
    # Movements
    MovementViewSet,
    # Lookups
    CategoryLookupViewSet,
    BrandLookupViewSet,
    VendorLookupViewSet,
    WarehouseLookupViewSet,
    ItemModelLookupViewSet,
    StockItemLookupViewSet,
)

# Router for CRUD ViewSets
router = DefaultRouter(trailing_slash=True)
router.register("categories", CategoryViewSet, basename="stock-categories")
router.register("brands", BrandViewSet, basename="stock-brands")
router.register("vendors", VendorViewSet, basename="stock-vendors")
router.register("item-models", ItemModelViewSet, basename="stock-item-models")
router.register("warehouses", WarehouseViewSet, basename="stock-warehouses")
router.register("items", StockItemViewSet, basename="stock-items")
router.register("movements", MovementViewSet, basename="stock-movements")

# Router for lookup ViewSets
lookup_router = DefaultRouter(trailing_slash=True)
lookup_router.register("categories", CategoryLookupViewSet, basename="lookup-categories")
lookup_router.register("brands", BrandLookupViewSet, basename="lookup-brands")
lookup_router.register("vendors", VendorLookupViewSet, basename="lookup-vendors")
lookup_router.register("warehouses", WarehouseLookupViewSet, basename="lookup-warehouses")
lookup_router.register("item-models", ItemModelLookupViewSet, basename="lookup-item-models")
lookup_router.register("items", StockItemLookupViewSet, basename="lookup-items")

urlpatterns = [
    # CRUD endpoints via router
    path("", include(router.urls)),

    # Command endpoints — Receive
    path("receive/quantity/", ReceiveQuantityView.as_view(), name="stock-receive-quantity"),
    path("receive/serialized/", ReceiveSerializedView.as_view(), name="stock-receive-serialized"),

    # Command endpoints — Issue
    path("issue/quantity/", IssueQuantityView.as_view(), name="stock-issue-quantity"),
    path("issue/serialized/", IssueSerializedView.as_view(), name="stock-issue-serialized"),

    # Command endpoints — Transfer
    path("transfer/quantity/", TransferQuantityView.as_view(), name="stock-transfer-quantity"),
    path("transfer/serialized/", TransferSerializedView.as_view(), name="stock-transfer-serialized"),

    # Adjustment endpoints
    path("adjustments/", CreateAdjustmentSessionView.as_view(), name="stock-adjustment-create"),
    path("adjustments/<uuid:session_id>/lines/", UpsertAdjustmentLinesView.as_view(), name="stock-adjustment-lines"),
    path("adjustments/<uuid:session_id>/confirm/", ConfirmAdjustmentSessionView.as_view(), name="stock-adjustment-confirm"),
    path("adjustments/<uuid:session_id>/cancel/", CancelAdjustmentSessionView.as_view(), name="stock-adjustment-cancel"),

    # Alert endpoints
    path("alerts/", AlertListView.as_view(), name="stock-alert-list"),
    path("alerts/<uuid:alert_id>/acknowledge/", AcknowledgeAlertView.as_view(), name="stock-alert-acknowledge"),
    path("alerts/<uuid:alert_id>/resolve/", ResolveAlertView.as_view(), name="stock-alert-resolve"),

    # Dashboard endpoints
    path("dashboard/summary/", DashboardSummaryView.as_view(), name="stock-dashboard-summary"),
    path("dashboard/recent-movements/", DashboardRecentMovementsView.as_view(), name="stock-dashboard-recent"),
    path("dashboard/low-stock/", DashboardLowStockView.as_view(), name="stock-dashboard-low-stock"),

    # Lookup endpoints
    path("lookups/", include(lookup_router.urls)),
]
