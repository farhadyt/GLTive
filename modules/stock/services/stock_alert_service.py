# Purpose: Business service for stock alert operations
from django.utils import timezone

from audit.services.logger import AuditService
from modules.stock.models.alert import StockAlertRule, StockAlertEvent
from modules.stock.services.exceptions import StockNotFoundError, StockValidationError
from modules.stock.services.utils import snapshot

ENTITY_TYPE = "stock_alert_event"


class StockAlertService:

    @staticmethod
    def evaluate_alerts_for_stock_item(company, stock_item, actor=None):
        """
        Automatic post-operation evaluator.
        Intended to run after receive/issue/transfer/adjustment flows.
        Does NOT write a separate audit log event; the created events are the trail.
        """
        rules = StockAlertRule.objects.filter(
            company=company,
            stock_item=stock_item,
            is_active=True
        )

        created_event_ids = []

        for rule in rules:
            if rule.rule_type == StockAlertRule.RULE_MINIMUM_STOCK:
                if stock_item.quantity_available <= rule.threshold_value:
                    is_already_open = StockAlertEvent.objects.filter(
                        company=company,
                        stock_item=stock_item,
                        alert_type=StockAlertRule.RULE_MINIMUM_STOCK,
                        status=StockAlertEvent.STATUS_OPEN
                    ).exists()

                    if not is_already_open:
                        event = StockAlertEvent.objects.create(
                            company=company,
                            stock_item=stock_item,
                            alert_rule=rule,
                            alert_type=StockAlertRule.RULE_MINIMUM_STOCK,
                            triggered_value=stock_item.quantity_available,
                            threshold_value=rule.threshold_value,
                            status=StockAlertEvent.STATUS_OPEN
                        )
                        created_event_ids.append(str(event.pk))

        return created_event_ids

    @staticmethod
    def acknowledge_alert(company, alert_event_id, actor):
        event = StockAlertEvent.objects.filter(company=company, pk=alert_event_id).first()
        if not event:
            raise StockNotFoundError(entity_type="stock_alert_event", entity_id=alert_event_id)

        if event.status != StockAlertEvent.STATUS_OPEN:
            raise StockValidationError(f"Cannot acknowledge alert in status: {event.status}")

        before = snapshot(event)
        event.status = StockAlertEvent.STATUS_ACKNOWLEDGED
        event.acknowledged_by = actor
        event.acknowledged_at = timezone.now()
        event.save()

        AuditService.log_event(
            action_code="stock.alert.acknowledged",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(event.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(event)
        )

        return event

    @staticmethod
    def resolve_alert(company, alert_event_id, actor):
        event = StockAlertEvent.objects.filter(company=company, pk=alert_event_id).first()
        if not event:
            raise StockNotFoundError(entity_type="stock_alert_event", entity_id=alert_event_id)

        if event.status not in [StockAlertEvent.STATUS_OPEN, StockAlertEvent.STATUS_ACKNOWLEDGED]:
            raise StockValidationError(f"Cannot resolve alert in status: {event.status}")

        before = snapshot(event)
        event.status = StockAlertEvent.STATUS_RESOLVED
        event.resolved_by = actor
        event.resolved_at = timezone.now()
        event.save()

        AuditService.log_event(
            action_code="stock.alert.resolved",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(event.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(event)
        )

        return event
