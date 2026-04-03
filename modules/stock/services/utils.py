# Purpose: Shared helpers for stock service layer
"""
Stock Service Utilities
Local helpers for snapshot generation, normalization, and entity fetching.
"""
from modules.stock.services.exceptions import StockNotFoundError


def get_company_entity(model_class, company, entity_id, *, active_only=False, entity_name=None):
    """
    Fetch a single entity within company scope.
    Raises StockNotFoundError if not found.
    """
    name = entity_name or model_class.__name__
    filters = {"company": company, "pk": entity_id}
    if active_only:
        filters["is_active"] = True
        filters["is_deleted"] = False
    try:
        return model_class.objects.get(**filters)
    except model_class.DoesNotExist:
        raise StockNotFoundError(entity_type=name, entity_id=entity_id)


def snapshot(instance):
    """
    Build a JSON-safe dict snapshot of a model instance for audit logging.
    Safely converts UUIDs, datetimes, Decimals, and ForeignKey references.
    """
    from decimal import Decimal
    import uuid as _uuid
    from datetime import datetime, date

    data = {}
    for field in instance._meta.concrete_fields:
        value = getattr(instance, field.attname)
        if value is None:
            data[field.attname] = None
        elif isinstance(value, _uuid.UUID):
            data[field.attname] = str(value)
        elif isinstance(value, (datetime, date)):
            data[field.attname] = value.isoformat()
        elif isinstance(value, Decimal):
            data[field.attname] = str(value)
        elif isinstance(value, bool):
            data[field.attname] = value
        elif isinstance(value, (int, float, str)):
            data[field.attname] = value
        else:
            data[field.attname] = str(value)
    return data


def normalize_name(value):
    """Normalize a name string for uniqueness comparison: strip + casefold."""
    if value is None:
        return None
    return value.strip().casefold()


def normalize_code(value):
    """Normalize a code string: strip + upper."""
    if value is None:
        return None
    return value.strip().upper()
