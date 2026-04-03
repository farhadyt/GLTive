# Purpose: Business service for stock receiving operations
"""
Stock Receive Service
Handles receiving quantity-based and serialized stock into inventory.
"""
from django.db import IntegrityError, transaction
from django.utils import timezone

from audit.services.logger import AuditService
from modules.stock.models.movement import StockMovement
from modules.stock.models.serial_unit import StockSerialUnit
from modules.stock.models.stock_item import StockItem
from modules.stock.services.exceptions import (
    StockConflictError,
    StockNotFoundError,
    StockValidationError,
)
from modules.stock.services.utils import snapshot

ENTITY_TYPE = "stock_item"


class StockReceiveService:
    """Business logic for receiving stock into inventory."""

    @staticmethod
    @transaction.atomic
    def receive_quantity_stock(company, data: dict, actor):
        stock_item_id = data.get("stock_item_id")
        quantity = data.get("quantity")

        if not stock_item_id:
            raise StockValidationError("stock_item_id is required", field="stock_item_id")
        if not quantity or quantity <= 0:
            raise StockValidationError("quantity must be greater than 0", field="quantity")

        unit_cost = data.get("unit_cost")
        if unit_cost is not None and unit_cost < 0:
            raise StockValidationError("unit_cost must be >= 0", field="unit_cost")

        # Lock stock item row before reading quantities
        stock_item = StockItem.objects.select_for_update().filter(
            company=company, pk=stock_item_id,
            is_active=True, is_deleted=False,
        ).first()
        if stock_item is None:
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=stock_item_id)

        if stock_item.tracking_type != "quantity_based":
            raise StockValidationError(
                "This stock item uses serialized tracking. Use receive_serialized_stock instead.",
                field="tracking_type",
            )

        # Validate warehouse is active
        if not stock_item.warehouse.is_active or stock_item.warehouse.is_deleted:
            raise StockValidationError(
                "The warehouse for this stock item is not active",
                field="warehouse",
            )

        now = timezone.now()
        before = snapshot(stock_item)

        # Update quantities
        stock_item.quantity_on_hand += quantity
        stock_item.quantity_available = stock_item.quantity_on_hand - stock_item.quantity_reserved
        stock_item.last_received_at = now
        stock_item.updated_by = actor
        stock_item.save(update_fields=[
            "quantity_on_hand", "quantity_available", "last_received_at", "updated_by",
        ])

        # Create immutable movement record
        movement = StockMovement.objects.create(
            company=company,
            movement_type=StockMovement.TYPE_STOCK_IN,
            stock_item=stock_item,
            stock_serial_unit=None,
            source_warehouse=None,
            target_warehouse=stock_item.warehouse,
            quantity=quantity,
            unit_cost=unit_cost,
            reference_type=data.get("reference_type"),
            reference_id=data.get("reference_id"),
            reason_code=data.get("reason_code"),
            note=data.get("note", ""),
            performed_by=actor,
            performed_at=now,
        )

        AuditService.log_event(
            action_code="stock.receive.quantity",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(stock_item.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
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
    def receive_serialized_stock(company, data: dict, actor):
        stock_item_id = data.get("stock_item_id")
        units = data.get("units")

        if not stock_item_id:
            raise StockValidationError("stock_item_id is required", field="stock_item_id")
        if not units or not isinstance(units, list) or len(units) == 0:
            raise StockValidationError("units list must be non-empty", field="units")

        unit_cost = data.get("unit_cost")

        # Lock stock item row before reading quantities
        stock_item = StockItem.objects.select_for_update().filter(
            company=company, pk=stock_item_id,
            is_active=True, is_deleted=False,
        ).first()
        if stock_item is None:
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=stock_item_id)

        if stock_item.tracking_type != "serialized":
            raise StockValidationError(
                "This stock item uses quantity tracking. Use receive_quantity_stock instead.",
                field="tracking_type",
            )

        # Validate warehouse is active
        if not stock_item.warehouse.is_active or stock_item.warehouse.is_deleted:
            raise StockValidationError(
                "The warehouse for this stock item is not active",
                field="warehouse",
            )

        now = timezone.now()
        before = snapshot(stock_item)
        serial_unit_ids = []
        movement_ids = []

        for idx, unit_data in enumerate(units):
            serial_number = unit_data.get("serial_number")
            if not serial_number:
                raise StockValidationError(
                    f"serial_number is required for unit at index {idx}",
                    field="serial_number",
                )

            # Serial uniqueness pre-check: condition=Q(is_deleted=False)
            if StockSerialUnit.objects.filter(
                company=company, serial_number=serial_number,
                is_deleted=False,
            ).exists():
                raise StockConflictError(
                    f"Serial number '{serial_number}' already exists in this company"
                )

            # Asset tag uniqueness pre-check: condition=Q(is_deleted=False, asset_tag_candidate__isnull=False)
            asset_tag = unit_data.get("asset_tag_candidate")
            if asset_tag:
                if StockSerialUnit.objects.filter(
                    company=company, asset_tag_candidate=asset_tag,
                    is_deleted=False,
                ).exists():
                    raise StockConflictError(
                        f"Asset tag '{asset_tag}' already exists in this company"
                    )

            # Create with IntegrityError race protection
            try:
                serial_unit = StockSerialUnit.objects.create(
                    company=company,
                    stock_item=stock_item,
                    warehouse=stock_item.warehouse,
                    serial_number=serial_number,
                    asset_tag_candidate=asset_tag or None,
                    condition_status=unit_data.get("condition_status", StockSerialUnit.CONDITION_NEW),
                    stock_status=StockSerialUnit.STATUS_IN_STOCK,
                    received_at=now,
                    notes=unit_data.get("note", ""),
                    is_active=True,
                    created_by=actor,
                    updated_by=actor,
                )
            except IntegrityError:
                raise StockConflictError(
                    f"A serial unit with serial number '{serial_number}' or asset tag "
                    f"'{asset_tag or ''}' was created concurrently"
                )

            serial_unit_ids.append(str(serial_unit.pk))

            movement = StockMovement.objects.create(
                company=company,
                movement_type=StockMovement.TYPE_STOCK_IN,
                stock_item=stock_item,
                stock_serial_unit=serial_unit,
                source_warehouse=None,
                target_warehouse=stock_item.warehouse,
                quantity=1,
                unit_cost=unit_cost,
                reference_type=data.get("reference_type"),
                reference_id=data.get("reference_id"),
                reason_code=data.get("reason_code"),
                note=data.get("note", ""),
                performed_by=actor,
                performed_at=now,
            )
            movement_ids.append(str(movement.pk))

        # Update stock item quantities
        stock_item.quantity_on_hand += len(units)
        stock_item.quantity_available = stock_item.quantity_on_hand - stock_item.quantity_reserved
        stock_item.last_received_at = now
        stock_item.updated_by = actor
        stock_item.save(update_fields=[
            "quantity_on_hand", "quantity_available", "last_received_at", "updated_by",
        ])

        AuditService.log_event(
            action_code="stock.receive.serialized",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(stock_item.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(stock_item),
            metadata={
                "serial_unit_ids": serial_unit_ids,
                "movement_ids": movement_ids,
                "units_received": len(units),
            },
        )

        return {
            "stock_item_id": str(stock_item.pk),
            "serial_unit_ids": serial_unit_ids,
            "movement_ids": movement_ids,
            "new_quantity_on_hand": stock_item.quantity_on_hand,
            "new_quantity_available": stock_item.quantity_available,
        }
