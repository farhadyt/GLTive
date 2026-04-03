# Purpose: Business service for stock transfer operations
"""
Stock Transfer Service
Handles transferring quantity-based and serialized stock between warehouses.
"""
from django.db import IntegrityError, transaction
from django.utils import timezone

from audit.services.logger import AuditService
from modules.stock.models.movement import StockMovement
from modules.stock.models.serial_unit import StockSerialUnit
from modules.stock.models.stock_item import StockItem
from modules.stock.models.warehouse import Warehouse
from modules.stock.services.exceptions import (
    StockNotFoundError,
    StockValidationError,
)
from modules.stock.services.utils import get_company_entity, snapshot

ENTITY_TYPE = "stock_item"


def _get_or_create_target_stock_item(company, source_stock_item, target_warehouse, actor):
    """
    Race-safe find-or-create for the target StockItem.
    Handles concurrent creation via IntegrityError catch + re-fetch.
    DB constraint: unique(company, warehouse, item_model) where is_deleted=False.
    """
    # Attempt lookup first
    target = StockItem.objects.select_for_update().filter(
        company=company,
        warehouse=target_warehouse,
        item_model=source_stock_item.item_model,
        is_deleted=False,
    ).first()

    if target is not None:
        return target

    # No existing target — attempt creation
    try:
        target = StockItem.objects.create(
            company=company,
            item_model=source_stock_item.item_model,
            warehouse=target_warehouse,
            internal_code=None,
            item_name_override=source_stock_item.item_name_override,
            tracking_type=source_stock_item.tracking_type,
            quantity_on_hand=0,
            quantity_reserved=0,
            quantity_available=0,
            minimum_stock_level_override=source_stock_item.minimum_stock_level_override,
            notes="",
            is_active=True,
            created_by=actor,
            updated_by=actor,
        )
        return target
    except IntegrityError:
        # Concurrent create race — re-fetch the row created by the other transaction
        target = StockItem.objects.select_for_update().filter(
            company=company,
            warehouse=target_warehouse,
            item_model=source_stock_item.item_model,
            is_deleted=False,
        ).first()
        if target is not None:
            return target
        # If still not found after IntegrityError, something is seriously wrong
        raise


class StockTransferService:
    """Business logic for transferring stock between warehouses."""

    @staticmethod
    @transaction.atomic
    def transfer_quantity_stock(company, data: dict, actor):
        source_stock_item_id = data.get("source_stock_item_id")
        target_warehouse_id = data.get("target_warehouse_id")
        quantity = data.get("quantity")

        if not source_stock_item_id:
            raise StockValidationError("source_stock_item_id is required", field="source_stock_item_id")
        if not target_warehouse_id:
            raise StockValidationError("target_warehouse_id is required", field="target_warehouse_id")
        if not quantity or quantity <= 0:
            raise StockValidationError("quantity must be greater than 0", field="quantity")

        # Lock source stock item
        source = StockItem.objects.select_for_update().filter(
            company=company, pk=source_stock_item_id,
            is_active=True, is_deleted=False,
        ).first()
        if source is None:
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=source_stock_item_id)

        if source.tracking_type != "quantity_based":
            raise StockValidationError(
                "This stock item uses serialized tracking. Use transfer_serialized_stock instead.",
                field="tracking_type",
            )

        # Fetch target warehouse
        target_warehouse = get_company_entity(
            Warehouse, company, target_warehouse_id,
            active_only=True, entity_name="stock_warehouse",
        )

        if source.warehouse_id == target_warehouse.pk:
            raise StockValidationError(
                "Source and target warehouses must be different",
                field="target_warehouse_id",
            )

        # Validate sufficient available stock
        if source.quantity_available < quantity:
            raise StockValidationError("Insufficient stock for transfer", field="quantity")

        # Race-safe find-or-create target stock item
        target = _get_or_create_target_stock_item(company, source, target_warehouse, actor)

        now = timezone.now()

        # Update source quantities
        source.quantity_on_hand -= quantity
        source.quantity_available = source.quantity_on_hand - source.quantity_reserved
        source.save(update_fields=["quantity_on_hand", "quantity_available"])

        # Update target quantities
        target.quantity_on_hand += quantity
        target.quantity_available = target.quantity_on_hand - target.quantity_reserved
        target.save(update_fields=["quantity_on_hand", "quantity_available"])

        # Create paired movements
        movement_out = StockMovement.objects.create(
            company=company,
            movement_type=StockMovement.TYPE_TRANSFER_OUT,
            stock_item=source,
            stock_serial_unit=None,
            source_warehouse=source.warehouse,
            target_warehouse=target_warehouse,
            quantity=quantity,
            unit_cost=None,
            reference_type=None,
            reference_id=None,
            reason_code=data.get("reason_code"),
            note=data.get("note", ""),
            performed_by=actor,
            performed_at=now,
        )

        movement_in = StockMovement.objects.create(
            company=company,
            movement_type=StockMovement.TYPE_TRANSFER_IN,
            stock_item=target,
            stock_serial_unit=None,
            source_warehouse=source.warehouse,
            target_warehouse=target_warehouse,
            quantity=quantity,
            unit_cost=None,
            reference_type=None,
            reference_id=None,
            reason_code=data.get("reason_code"),
            note=data.get("note", ""),
            performed_by=actor,
            performed_at=now,
        )

        AuditService.log_event(
            action_code="stock.transfer.quantity",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(source.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(source),
            metadata={
                "source_stock_item_id": str(source.pk),
                "target_stock_item_id": str(target.pk),
                "target_warehouse_id": str(target_warehouse.pk),
                "quantity": str(quantity),
                "movement_out_id": str(movement_out.pk),
                "movement_in_id": str(movement_in.pk),
            },
        )

        return {
            "source_stock_item_id": str(source.pk),
            "target_stock_item_id": str(target.pk),
            "movement_ids": [str(movement_out.pk), str(movement_in.pk)],
            "new_source_quantity_on_hand": source.quantity_on_hand,
            "new_target_quantity_on_hand": target.quantity_on_hand,
        }

    @staticmethod
    @transaction.atomic
    def transfer_serialized_stock(company, data: dict, actor):
        source_stock_item_id = data.get("source_stock_item_id")
        target_warehouse_id = data.get("target_warehouse_id")
        serial_unit_ids = data.get("serial_unit_ids")

        if not source_stock_item_id:
            raise StockValidationError("source_stock_item_id is required", field="source_stock_item_id")
        if not target_warehouse_id:
            raise StockValidationError("target_warehouse_id is required", field="target_warehouse_id")
        if not serial_unit_ids or not isinstance(serial_unit_ids, list) or len(serial_unit_ids) == 0:
            raise StockValidationError("serial_unit_ids must be non-empty", field="serial_unit_ids")

        # Lock source stock item
        source = StockItem.objects.select_for_update().filter(
            company=company, pk=source_stock_item_id,
            is_active=True, is_deleted=False,
        ).first()
        if source is None:
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=source_stock_item_id)

        if source.tracking_type != "serialized":
            raise StockValidationError(
                "This stock item uses quantity tracking. Use transfer_quantity_stock instead.",
                field="tracking_type",
            )

        # Fetch target warehouse
        target_warehouse = get_company_entity(
            Warehouse, company, target_warehouse_id,
            active_only=True, entity_name="stock_warehouse",
        )

        if source.warehouse_id == target_warehouse.pk:
            raise StockValidationError(
                "Source and target warehouses must be different",
                field="target_warehouse_id",
            )

        # Race-safe find-or-create target stock item
        target = _get_or_create_target_stock_item(company, source, target_warehouse, actor)

        now = timezone.now()
        movement_ids = []

        for unit_id in serial_unit_ids:
            # Lock serial unit before status check
            serial_unit = StockSerialUnit.objects.select_for_update().filter(
                company=company,
                pk=unit_id,
                stock_item=source,
                is_deleted=False,
            ).first()
            if serial_unit is None:
                raise StockNotFoundError(entity_type="stock_serial_unit", entity_id=unit_id)

            if serial_unit.stock_status != StockSerialUnit.STATUS_IN_STOCK:
                raise StockValidationError(
                    f"Serial unit '{serial_unit.serial_number}' is not in_stock (current: {serial_unit.stock_status})",
                    field="serial_unit_ids",
                )

            # Move the unit to target
            serial_unit.stock_item = target
            serial_unit.warehouse = target_warehouse
            serial_unit.updated_by = actor
            serial_unit.save(update_fields=["stock_item_id", "warehouse_id", "updated_by"])

            # Create paired movements
            movement_out = StockMovement.objects.create(
                company=company,
                movement_type=StockMovement.TYPE_TRANSFER_OUT,
                stock_item=source,
                stock_serial_unit=serial_unit,
                source_warehouse=source.warehouse,
                target_warehouse=target_warehouse,
                quantity=1,
                unit_cost=None,
                reference_type=None,
                reference_id=None,
                reason_code=data.get("reason_code"),
                note=data.get("note", ""),
                performed_by=actor,
                performed_at=now,
            )

            movement_in = StockMovement.objects.create(
                company=company,
                movement_type=StockMovement.TYPE_TRANSFER_IN,
                stock_item=target,
                stock_serial_unit=serial_unit,
                source_warehouse=source.warehouse,
                target_warehouse=target_warehouse,
                quantity=1,
                unit_cost=None,
                reference_type=None,
                reference_id=None,
                reason_code=data.get("reason_code"),
                note=data.get("note", ""),
                performed_by=actor,
                performed_at=now,
            )

            movement_ids.extend([str(movement_out.pk), str(movement_in.pk)])

        # Update source quantities
        source.quantity_on_hand -= len(serial_unit_ids)
        source.quantity_available = source.quantity_on_hand - source.quantity_reserved
        source.save(update_fields=["quantity_on_hand", "quantity_available"])

        # Update target quantities
        target.quantity_on_hand += len(serial_unit_ids)
        target.quantity_available = target.quantity_on_hand - target.quantity_reserved
        target.save(update_fields=["quantity_on_hand", "quantity_available"])

        AuditService.log_event(
            action_code="stock.transfer.serialized",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(source.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(source),
            metadata={
                "source_stock_item_id": str(source.pk),
                "target_stock_item_id": str(target.pk),
                "target_warehouse_id": str(target_warehouse.pk),
                "serial_unit_ids": [str(uid) for uid in serial_unit_ids],
                "movement_ids": movement_ids,
                "units_transferred": len(serial_unit_ids),
            },
        )

        return {
            "source_stock_item_id": str(source.pk),
            "target_stock_item_id": str(target.pk),
            "serial_unit_ids": [str(uid) for uid in serial_unit_ids],
            "movement_ids": movement_ids,
            "new_source_quantity_on_hand": source.quantity_on_hand,
            "new_target_quantity_on_hand": target.quantity_on_hand,
        }
