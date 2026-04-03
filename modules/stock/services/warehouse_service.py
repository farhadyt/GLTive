# Purpose: Business service for Warehouse master data
"""
Warehouse Service
Company-scoped CRUD, deactivation, and default-swap logic for warehouses.
"""
from django.db import transaction

from audit.services.logger import AuditService
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
    normalize_code,
    snapshot,
)

ENTITY_TYPE = "stock_warehouse"


class WarehouseService:
    """Business logic for warehouse management."""

    @staticmethod
    @transaction.atomic
    def create_warehouse(company, data: dict, actor):
        code = data.get("code")
        name = data.get("name")

        if not code:
            raise StockValidationError("code is required", field="code")
        if not name:
            raise StockValidationError("name is required", field="name")

        code = normalize_code(code)

        if Warehouse.objects.filter(
            company=company, code=code, is_active=True, is_deleted=False,
        ).exists():
            raise StockConflictError(
                f"Active warehouse with code '{code}' already exists in this company"
            )

        is_default = data.get("is_default", False)

        # If no active warehouses exist, force default
        has_warehouses = Warehouse.objects.filter(
            company=company, is_active=True, is_deleted=False,
        ).exists()
        if not has_warehouses:
            is_default = True

        # If requesting default, clear old default atomically
        if is_default:
            Warehouse.objects.select_for_update().filter(
                company=company, is_default=True, is_active=True, is_deleted=False,
            ).update(is_default=False)

        warehouse = Warehouse.objects.create(
            company=company,
            code=code,
            name=name.strip(),
            location_reference_id=data.get("location_reference_id"),
            description=data.get("description", ""),
            is_default=is_default,
            is_active=True,
            created_by=actor,
            updated_by=actor,
        )

        AuditService.log_event(
            action_code="stock.warehouse.created",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(warehouse.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(warehouse),
        )

        return warehouse

    @staticmethod
    def update_warehouse(company, warehouse_id, data: dict, actor):
        warehouse = get_company_entity(
            Warehouse, company, warehouse_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )
        before = snapshot(warehouse)

        if "code" in data:
            new_code = normalize_code(data["code"])
            if new_code != warehouse.code:
                if Warehouse.objects.filter(
                    company=company, code=new_code,
                    is_active=True, is_deleted=False,
                ).exclude(pk=warehouse.pk).exists():
                    raise StockConflictError(
                        f"Active warehouse with code '{new_code}' already exists in this company"
                    )
                warehouse.code = new_code

        if "is_default" in data:
            raise StockValidationError(
                "Use set_default_warehouse to change default warehouse",
                field="is_default",
            )

        if "name" in data:
            warehouse.name = data["name"].strip()

        if "location_reference_id" in data:
            warehouse.location_reference_id = data["location_reference_id"]

        if "description" in data:
            warehouse.description = data["description"]

        warehouse.updated_by = actor
        warehouse.save()

        AuditService.log_event(
            action_code="stock.warehouse.updated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(warehouse.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(warehouse),
        )

        return warehouse

    @staticmethod
    @transaction.atomic
    def deactivate_warehouse(company, warehouse_id, actor):
        warehouse = Warehouse.objects.select_for_update().filter(
            company=company, pk=warehouse_id,
            is_active=True, is_deleted=False,
        ).first()
        if warehouse is None:
            from modules.stock.services.exceptions import StockNotFoundError
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=warehouse_id)

        # Blocker 1: default warehouse
        if warehouse.is_default:
            raise StockValidationError(
                "Cannot deactivate default warehouse. Assign another warehouse as default first.",
                field="is_default",
            )

        # Blocker 2: active stock items with available quantity
        stock_count = StockItem.objects.filter(
            company=company, warehouse=warehouse,
            is_active=True, is_deleted=False,
            quantity_available__gt=0,
        ).count()
        if stock_count > 0:
            raise StockDeactivationBlockedError(
                entity_type=ENTITY_TYPE,
                reason=f"{stock_count} active stock items with available quantity remain in this warehouse",
                blocking_count=stock_count,
            )

        # Blocker 3: active serial units in operational states
        serial_count = StockSerialUnit.objects.filter(
            company=company, warehouse=warehouse,
            is_deleted=False,
            stock_status__in=[
                StockSerialUnit.STATUS_IN_STOCK,
                StockSerialUnit.STATUS_RESERVED,
            ],
        ).count()
        if serial_count > 0:
            raise StockDeactivationBlockedError(
                entity_type=ENTITY_TYPE,
                reason=f"{serial_count} active serial units (in_stock/reserved) remain in this warehouse",
                blocking_count=serial_count,
            )

        before = snapshot(warehouse)
        warehouse.is_active = False
        warehouse.updated_by = actor
        warehouse.save()

        AuditService.log_event(
            action_code="stock.warehouse.deactivated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(warehouse.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(warehouse),
        )

        return warehouse

    @staticmethod
    @transaction.atomic
    def set_default_warehouse(company, warehouse_id, actor):
        warehouse = Warehouse.objects.select_for_update().filter(
            company=company, pk=warehouse_id,
            is_active=True, is_deleted=False,
        ).first()
        if warehouse is None:
            from modules.stock.services.exceptions import StockNotFoundError
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=warehouse_id)

        before = snapshot(warehouse)

        # Clear old defaults
        Warehouse.objects.select_for_update().filter(
            company=company, is_default=True, is_active=True, is_deleted=False,
        ).exclude(pk=warehouse.pk).update(is_default=False)

        warehouse.is_default = True
        warehouse.updated_by = actor
        warehouse.save()

        AuditService.log_event(
            action_code="stock.warehouse.default_changed",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(warehouse.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(warehouse),
        )

        return warehouse
