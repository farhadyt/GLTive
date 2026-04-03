# Purpose: Business service for stock module dashboard metrics and summaries
from datetime import timedelta
from django.utils import timezone

from modules.stock.models.alert import StockAlertEvent
from modules.stock.models.movement import StockMovement
from modules.stock.models.stock_item import StockItem
from modules.stock.models.warehouse import Warehouse


class StockDashboardService:

    @staticmethod
    def get_summary(company):
        """
        Returns a high-level summary of the stock module for the given company.
        """
        now = timezone.now()
        
        total_active_stock_items = StockItem.objects.filter(
            company=company, is_active=True, is_deleted=False
        ).count()
        
        total_warehouses = Warehouse.objects.filter(
            company=company, is_active=True, is_deleted=False
        ).count()
        
        low_stock_count = StockAlertEvent.objects.filter(
            company=company, status=StockAlertEvent.STATUS_OPEN
        ).values("stock_item").distinct().count()
        
        recent_movements_count = StockMovement.objects.filter(
            company=company, performed_at__gte=now - timedelta(days=7)
        ).count()
        
        serialized_count = StockItem.objects.filter(
            company=company, is_active=True, is_deleted=False, tracking_type="serialized"
        ).count()
        
        quantity_based_count = StockItem.objects.filter(
            company=company, is_active=True, is_deleted=False, tracking_type="quantity_based"
        ).count()
        
        return {
            "total_active_stock_items": total_active_stock_items,
            "total_warehouses": total_warehouses,
            "low_stock_count": low_stock_count,
            "recent_movements_count": recent_movements_count,
            "serialized_count": serialized_count,
            "quantity_based_count": quantity_based_count,
        }

    @staticmethod
    def get_recent_movements(company, limit=10):
        movements = StockMovement.objects.filter(
            company=company
        ).select_related(
            "stock_item",
            "stock_item__item_model",
            "source_warehouse",
            "target_warehouse",
            "performed_by",
        ).order_by("-performed_at")[:limit]

        results = []
        for mv in movements:
            stock_item_name = mv.stock_item.item_name_override or mv.stock_item.item_model.model_name
            results.append({
                "id": str(mv.id),
                "movement_type": str(mv.movement_type),
                "stock_item_id": str(mv.stock_item.id),
                "stock_item_name": str(stock_item_name),
                "quantity": str(mv.quantity),
                "performed_at": mv.performed_at.isoformat(),
                "performed_by_username": str(mv.performed_by.username) if mv.performed_by else None,
                "source_warehouse_name": str(mv.source_warehouse.name) if mv.source_warehouse else None,
                "target_warehouse_name": str(mv.target_warehouse.name) if mv.target_warehouse else None,
            })
        
        return results

    @staticmethod
    def get_low_stock_items(company, limit=20):
        alert_item_ids = StockAlertEvent.objects.filter(
            company=company,
            status=StockAlertEvent.STATUS_OPEN
        ).values_list("stock_item_id", flat=True).distinct()

        items = StockItem.objects.filter(
            company=company,
            pk__in=alert_item_ids,
            is_active=True,
            is_deleted=False,
        ).select_related(
            "item_model",
            "warehouse",
        )[:limit]

        results = []
        for item in items:
            item_name = item.item_name_override or item.item_model.model_name
            results.append({
                "id": str(item.id),
                "item_name": str(item_name),
                "warehouse_code": str(item.warehouse.code),
                "warehouse_name": str(item.warehouse.name),
                "quantity_on_hand": str(item.quantity_on_hand),
                "quantity_available": str(item.quantity_available),
                "tracking_type": str(item.tracking_type),
            })
            
        return results
