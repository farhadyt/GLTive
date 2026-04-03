# Purpose: Business service for StockItem management
"""
Stock Item Service
Company-scoped CRUD and lifecycle for stock item records.
"""
from audit.services.logger import AuditService
from modules.stock.models.item_model import ItemModel
from modules.stock.models.serial_unit import StockSerialUnit
from modules.stock.models.stock_item import StockItem
from modules.stock.models.warehouse import Warehouse
from modules.stock.services.exceptions import (
    StockConflictError,
    StockDeactivationBlockedError,
    StockValidationError,
)
from modules.stock.services.utils import (
    get_company_entity,
    snapshot,
)

ENTITY_TYPE = "stock_item"

IMMUTABLE_FIELDS = {"item_model_id", "warehouse_id", "tracking_type"}


class StockItemService:
    """Business logic for stock item management."""

    @staticmethod
    def create_stock_item(company, data: dict, actor):
        item_model_id = data.get("item_model_id")
        warehouse_id = data.get("warehouse_id")

        if not item_model_id:
            raise StockValidationError("item_model_id is required", field="item_model_id")
        if not warehouse_id:
            raise StockValidationError("warehouse_id is required", field="warehouse_id")

        item_model = get_company_entity(
            ItemModel, company, item_model_id,
            active_only=True, entity_name="stock_item_model",
        )
        warehouse = get_company_entity(
            Warehouse, company, warehouse_id,
            active_only=True, entity_name="stock_warehouse",
        )

        # Duplicate check: (company, warehouse, item_model) condition=Q(is_deleted=False)
        if StockItem.objects.filter(
            company=company, warehouse=warehouse, item_model=item_model,
            is_deleted=False,
        ).exists():
            raise StockConflictError(
                "A stock item for this item model already exists in this warehouse"
            )

        # internal_code duplicate check: condition=Q(is_deleted=False, internal_code__isnull=False)
        internal_code = data.get("internal_code")
        if internal_code:
            internal_code = internal_code.strip()
            if StockItem.objects.filter(
                company=company, internal_code=internal_code,
                is_deleted=False,
            ).exists():
                raise StockConflictError(
                    f"Stock item with internal code '{internal_code}' already exists in this company"
                )

        stock_item = StockItem.objects.create(
            company=company,
            item_model=item_model,
            warehouse=warehouse,
            internal_code=internal_code or None,
            item_name_override=data.get("item_name_override"),
            tracking_type=item_model.tracking_type,
            quantity_on_hand=0,
            quantity_reserved=0,
            quantity_available=0,
            minimum_stock_level_override=data.get("minimum_stock_level_override"),
            notes=data.get("notes", ""),
            is_active=True,
            created_by=actor,
            updated_by=actor,
        )

        AuditService.log_event(
            action_code="stock.item.created",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(stock_item.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(stock_item),
        )

        return stock_item

    @staticmethod
    def update_stock_item(company, stock_item_id, data: dict, actor):
        stock_item = get_company_entity(
            StockItem, company, stock_item_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )
        before = snapshot(stock_item)

        # Block immutable field changes
        for field in IMMUTABLE_FIELDS:
            if field in data:
                raise StockValidationError(
                    f"{field} cannot be changed after creation",
                    field=field,
                )

        if "internal_code" in data:
            new_code = data["internal_code"]
            if new_code:
                new_code = new_code.strip()
                if new_code != stock_item.internal_code:
                    if StockItem.objects.filter(
                        company=company, internal_code=new_code,
                        is_deleted=False,
                    ).exclude(pk=stock_item.pk).exists():
                        raise StockConflictError(
                            f"Stock item with internal code '{new_code}' already exists in this company"
                        )
                stock_item.internal_code = new_code
            else:
                stock_item.internal_code = None

        if "item_name_override" in data:
            stock_item.item_name_override = data["item_name_override"]

        if "minimum_stock_level_override" in data:
            stock_item.minimum_stock_level_override = data["minimum_stock_level_override"]

        if "notes" in data:
            stock_item.notes = data["notes"]

        stock_item.updated_by = actor
        stock_item.save()

        AuditService.log_event(
            action_code="stock.item.updated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(stock_item.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(stock_item),
        )

        return stock_item

    @staticmethod
    def deactivate_stock_item(company, stock_item_id, actor):
        stock_item = get_company_entity(
            StockItem, company, stock_item_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )

        # Blocker 1: quantity_on_hand > 0
        if stock_item.quantity_on_hand > 0:
            raise StockDeactivationBlockedError(
                entity_type=ENTITY_TYPE,
                reason="Stock item has quantity on hand",
                blocking_count=int(stock_item.quantity_on_hand),
            )

        # Blocker 2: active serial units in operational states
        serial_count = StockSerialUnit.objects.filter(
            company=company,
            stock_item=stock_item,
            is_deleted=False,
            stock_status__in=[
                StockSerialUnit.STATUS_IN_STOCK,
                StockSerialUnit.STATUS_RESERVED,
            ],
        ).count()
        if serial_count > 0:
            raise StockDeactivationBlockedError(
                entity_type=ENTITY_TYPE,
                reason=f"{serial_count} serial units with in_stock/reserved status remain",
                blocking_count=serial_count,
            )

        before = snapshot(stock_item)
        stock_item.is_active = False
        stock_item.updated_by = actor
        stock_item.save()

        AuditService.log_event(
            action_code="stock.item.deactivated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(stock_item.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(stock_item),
        )

        return stock_item

    @staticmethod
    def recalculate_available_quantity(stock_item):
        """Recalculate quantity_available from on_hand and reserved."""
        stock_item.quantity_available = stock_item.quantity_on_hand - stock_item.quantity_reserved
        stock_item.save(update_fields=["quantity_available"])
        return stock_item
