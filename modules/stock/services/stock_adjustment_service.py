# Purpose: Business service for stock adjustment operations
import random
import string
from django.db import transaction, IntegrityError
from django.utils import timezone

from audit.services.logger import AuditService
from modules.stock.models.adjustment import StockAdjustmentSession, StockAdjustmentLine
from modules.stock.models.movement import StockMovement
from modules.stock.models.stock_item import StockItem
from modules.stock.models.warehouse import Warehouse
from modules.stock.services.exceptions import StockConflictError, StockNotFoundError, StockValidationError
from modules.stock.services.utils import get_company_entity, snapshot

ENTITY_TYPE = "stock_adjustment_session"


def _generate_session_code():
    """Generates a session code like ADJ-20260404-A3KX9B"""
    date_part = timezone.now().strftime("%Y%m%d")
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ADJ-{date_part}-{random_part}"


class StockAdjustmentService:

    @staticmethod
    def create_adjustment_session(company, data: dict, actor):
        warehouse_id = data.get("warehouse_id")
        if not warehouse_id:
            raise StockValidationError("warehouse_id is required", field="warehouse_id")

        warehouse = get_company_entity(Warehouse, company, warehouse_id, active_only=True, entity_name="warehouse")

        reason = data.get("reason", "")
        session_code = _generate_session_code()

        # Try create once
        try:
            session = StockAdjustmentSession.objects.create(
                company=company,
                warehouse=warehouse,
                session_code=session_code,
                reason=reason,
                status="draft",
                created_by=actor
            )
        except IntegrityError:
            # Regenerate once and retry
            session_code = _generate_session_code()
            try:
                session = StockAdjustmentSession.objects.create(
                    company=company,
                    warehouse=warehouse,
                    session_code=session_code,
                    reason=reason,
                    status="draft",
                    created_by=actor
                )
            except IntegrityError:
                raise StockConflictError("Failed to generate a unique adjustment session code. Please try again.")

        AuditService.log_event(
            action_code="stock.adjustment.session_created",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(session.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(session),
        )

        return session

    @staticmethod
    @transaction.atomic
    def upsert_adjustment_lines(company, session_id, lines_data, actor):
        session = StockAdjustmentSession.objects.select_for_update().filter(
            company=company, pk=session_id
        ).first()

        if not session:
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=session_id)

        if session.status != "draft":
            raise StockValidationError(f"Cannot edit lines for session in status: {session.status}")

        if not lines_data or not isinstance(lines_data, list):
            raise StockValidationError("lines_data must be a non-empty list")
            
        results = []
        for line_data in lines_data:
            stock_item_id = line_data.get("stock_item_id")
            counted_quantity = line_data.get("counted_quantity")

            if not stock_item_id:
                raise StockValidationError("stock_item_id is required", field="stock_item_id")
            if counted_quantity is None or counted_quantity < 0:
                raise StockValidationError("counted_quantity must be >= 0", field="counted_quantity")

            stock_item = StockItem.objects.filter(
                company=company, pk=stock_item_id, is_active=True, is_deleted=False
            ).first()

            if not stock_item:
                raise StockNotFoundError(entity_type="stock_item", entity_id=stock_item_id)

            if stock_item.warehouse_id != session.warehouse_id:
                raise StockValidationError(
                    "stock_item warehouse does not match session warehouse",
                    field="stock_item_id"
                )

            expected_quantity = stock_item.quantity_on_hand
            difference_quantity = counted_quantity - expected_quantity

            line, created = StockAdjustmentLine.objects.update_or_create(
                adjustment_session=session,
                stock_item=stock_item,
                defaults={
                    "company": company,
                    "expected_quantity": expected_quantity,
                    "counted_quantity": counted_quantity,
                    "difference_quantity": difference_quantity,
                    "note": line_data.get("note", "")
                }
            )
            results.append(line)

        AuditService.log_event(
            action_code="stock.adjustment.lines_updated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(session.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(session),
            metadata={
                "session_id": str(session.pk),
                "line_count": len(results)
            }
        )

        return results

    @staticmethod
    @transaction.atomic
    def confirm_adjustment_session(company, session_id, actor):
        session = StockAdjustmentSession.objects.select_for_update().filter(
            company=company, pk=session_id
        ).first()

        if not session:
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=session_id)

        if session.status != "draft":
            raise StockValidationError(f"Cannot confirm session in status: {session.status}")

        lines = StockAdjustmentLine.objects.filter(company=company, adjustment_session=session)
        if not lines.exists():
            raise StockValidationError("Cannot confirm session with no adjustment lines")

        now = timezone.now()
        movement_ids = []
        lines_processed = 0

        for line in lines:
            stock_item = StockItem.objects.select_for_update().filter(
                company=company, pk=line.stock_item_id, is_active=True, is_deleted=False
            ).first()

            if not stock_item:
                raise StockValidationError(f"Missing stock item {line.stock_item_id}")

            before = snapshot(stock_item)

            if line.difference_quantity > 0:
                stock_item.quantity_on_hand += line.difference_quantity
                movement = StockMovement.objects.create(
                    company=company,
                    movement_type=StockMovement.TYPE_ADJUSTMENT_PLUS,
                    stock_item=stock_item,
                    stock_serial_unit=None,
                    source_warehouse=None,
                    target_warehouse=session.warehouse,
                    quantity=line.difference_quantity,
                    unit_cost=None,
                    reference_type="adjustment",
                    reference_id=str(session.id),
                    reason_code=None,
                    note=line.note or "",
                    performed_by=actor,
                    performed_at=now,
                )
                movement_ids.append(str(movement.pk))

            elif line.difference_quantity < 0:
                if stock_item.quantity_on_hand + line.difference_quantity < 0:
                    raise StockValidationError(f"Negative stock not allowed for item {stock_item.id}")
                
                stock_item.quantity_on_hand += line.difference_quantity
                movement = StockMovement.objects.create(
                    company=company,
                    movement_type=StockMovement.TYPE_ADJUSTMENT_MINUS,
                    stock_item=stock_item,
                    stock_serial_unit=None,
                    source_warehouse=session.warehouse,
                    target_warehouse=None,
                    quantity=abs(line.difference_quantity),
                    unit_cost=None,
                    reference_type="adjustment",
                    reference_id=str(session.id),
                    reason_code=None,
                    note=line.note or "",
                    performed_by=actor,
                    performed_at=now,
                )
                movement_ids.append(str(movement.pk))
            else:
                continue

            stock_item.quantity_available = stock_item.quantity_on_hand - stock_item.quantity_reserved
            stock_item.updated_by = actor
            stock_item.save(update_fields=[
                "quantity_on_hand", "quantity_available", "updated_by"
            ])
            lines_processed += 1

        session_before = snapshot(session)
        session.status = "confirmed"
        session.confirmed_by = actor
        session.confirmed_at = now
        session.save()

        AuditService.log_event(
            action_code="stock.adjustment.confirmed",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(session.pk),
            actor_user=actor,
            company=company,
            before_snapshot=session_before,
            after_snapshot=snapshot(session),
            metadata={
                "session_id": str(session.pk),
                "session_code": session.session_code,
                "line_count": lines.count(),
                "lines_processed": lines_processed,
                "movement_ids": movement_ids,
            }
        )

        return {
            "session_id": str(session.pk),
            "session_code": session.session_code,
            "status": "confirmed",
            "lines_processed": lines_processed,
            "movement_ids": movement_ids,
        }

    @staticmethod
    def cancel_adjustment_session(company, session_id, actor):
        session = StockAdjustmentSession.objects.filter(company=company, pk=session_id).first()
        if not session:
            raise StockNotFoundError(entity_type=ENTITY_TYPE, entity_id=session_id)

        if session.status != "draft":
            raise StockValidationError(f"Only draft sessions can be cancelled. Current status: {session.status}")

        before = snapshot(session)
        session.status = "cancelled"
        session.save()

        AuditService.log_event(
            action_code="stock.adjustment.cancelled",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(session.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(session),
        )

        return session
