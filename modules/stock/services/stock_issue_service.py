# Purpose: Business service for stock issuing operations
"""
Stock Issue Service
Handles issuing quantity-based and serialized stock from inventory.
"""
from django.db import transaction
from django.utils import timezone

from audit.services.logger import AuditService
from modules.stock.models.movement import StockMovement
from modules.stock.models.serial_unit import StockSerialUnit
from modules.stock.models.stock_item import StockItem
from modules.stock.services.exceptions import (
    StockNotFoundError,
    StockValidationError,
)
from modules.stock.services.utils import snapshot

ENTITY_TYPE = "stock_item"


class StockIssueService:
    """Business logic for issuing stock from inventory."""

    @staticmethod
    @transaction.atomic
    def issue_quantity_stock(company, data: dict, actor):
        stock_item_id = data.get("stock_item_id")
        quantity = data.get("quantity")

        if not stock_item_id:
            raise StockValidationError("stock_item_id is required", field="stock_item_id")
        if not quantity or quantity <= 0:
            raise StockValidationError("quantity must be greater than 0", field="quantity")

        # Lock stock item row before reading quantities
        stock_item = StockItem.objects.select_for_update().filter(
            company=company, pk=stock_item_id,
            is_active=True, is_deleted=False,
        ).first()
        if stock_item is None:
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=stock_item_id)

        if stock_item.tracking_type != "quantity_based":
            raise StockValidationError(
                "This stock item uses serialized tracking. Use issue_serialized_stock instead.",
                field="tracking_type",
            )

        # Validate warehouse is active
        if not stock_item.warehouse.is_active or stock_item.warehouse.is_deleted:
            raise StockValidationError(
                "The warehouse for this stock item is not active",
                field="warehouse",
            )

        # Validate sufficient available stock
        if stock_item.quantity_available < quantity:
            raise StockValidationError("Insufficient stock", field="quantity")

        now = timezone.now()

        # Update quantities
        stock_item.quantity_on_hand -= quantity
        stock_item.quantity_available = stock_item.quantity_on_hand - stock_item.quantity_reserved
        stock_item.last_issued_at = now
        stock_item.save(update_fields=[
            "quantity_on_hand", "quantity_available", "last_issued_at",
        ])

        # Create immutable movement record
        movement = StockMovement.objects.create(
            company=company,
            movement_type=StockMovement.TYPE_STOCK_OUT,
            stock_item=stock_item,
            stock_serial_unit=None,
            source_warehouse=stock_item.warehouse,
            target_warehouse=None,
            quantity=quantity,
            unit_cost=None,
            reference_type=data.get("reference_type"),
            reference_id=data.get("reference_id"),
            reason_code=data.get("reason_code"),
            note=data.get("note", ""),
            performed_by=actor,
            performed_at=now,
        )

        AuditService.log_event(
            action_code="stock.issue.quantity",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(stock_item.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(stock_item),
            metadata={"movement_id": str(movement.pk), "quantity": str(quantity)},
        )

        return {
            "stock_item_id": str(stock_item.pk),
            "movement_id": str(movement.pk),
            "new_quantity_on_hand": stock_item.quantity_on_hand,
            "new_quantity_available": stock_item.quantity_available,
        }

    @staticmethod
    @transaction.atomic
    def issue_serialized_stock(company, data: dict, actor):
        stock_item_id = data.get("stock_item_id")
        serial_unit_ids = data.get("serial_unit_ids")

        if not stock_item_id:
            raise StockValidationError("stock_item_id is required", field="stock_item_id")
        if not serial_unit_ids or not isinstance(serial_unit_ids, list) or len(serial_unit_ids) == 0:
            raise StockValidationError("serial_unit_ids must be non-empty", field="serial_unit_ids")

        # Lock stock item row
        stock_item = StockItem.objects.select_for_update().filter(
            company=company, pk=stock_item_id,
            is_active=True, is_deleted=False,
        ).first()
        if stock_item is None:
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=stock_item_id)

        if stock_item.tracking_type != "serialized":
            raise StockValidationError(
                "This stock item uses quantity tracking. Use issue_quantity_stock instead.",
                field="tracking_type",
            )

        # Validate warehouse is active
        if not stock_item.warehouse.is_active or stock_item.warehouse.is_deleted:
            raise StockValidationError(
                "The warehouse for this stock item is not active",
                field="warehouse",
            )

        now = timezone.now()
        movement_ids = []

        for unit_id in serial_unit_ids:
            # Lock serial unit before status check
            serial_unit = StockSerialUnit.objects.select_for_update().filter(
                company=company,
                pk=unit_id,
                stock_item=stock_item,
                is_deleted=False,
            ).first()
            if serial_unit is None:
                raise StockNotFoundError(entity_type="stock_serial_unit", entity_id=unit_id)

            if serial_unit.stock_status != StockSerialUnit.STATUS_IN_STOCK:
                raise StockValidationError(
                    f"Serial unit '{serial_unit.serial_number}' is not in_stock (current: {serial_unit.stock_status})",
                    field="serial_unit_ids",
                )

            serial_unit.stock_status = StockSerialUnit.STATUS_ISSUED
            serial_unit.updated_by = actor
            serial_unit.save(update_fields=["stock_status", "updated_by"])

            movement = StockMovement.objects.create(
                company=company,
                movement_type=StockMovement.TYPE_STOCK_OUT,
                stock_item=stock_item,
                stock_serial_unit=serial_unit,
                source_warehouse=stock_item.warehouse,
                target_warehouse=None,
                quantity=1,
                unit_cost=None,
                reference_type=data.get("reference_type"),
                reference_id=data.get("reference_id"),
                reason_code=data.get("reason_code"),
                note=data.get("note", ""),
                performed_by=actor,
                performed_at=now,
            )
            movement_ids.append(str(movement.pk))

        # Update stock item quantities
        stock_item.quantity_on_hand -= len(serial_unit_ids)
        stock_item.quantity_available = stock_item.quantity_on_hand - stock_item.quantity_reserved
        stock_item.last_issued_at = now
        stock_item.save(update_fields=[
            "quantity_on_hand", "quantity_available", "last_issued_at",
        ])

        AuditService.log_event(
            action_code="stock.issue.serialized",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(stock_item.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(stock_item),
            metadata={
                "serial_unit_ids": [str(uid) for uid in serial_unit_ids],
                "movement_ids": movement_ids,
                "units_issued": len(serial_unit_ids),
            },
        )

        return {
            "stock_item_id": str(stock_item.pk),
            "serial_unit_ids": [str(uid) for uid in serial_unit_ids],
            "movement_ids": movement_ids,
            "new_quantity_on_hand": stock_item.quantity_on_hand,
            "new_quantity_available": stock_item.quantity_available,
        }
