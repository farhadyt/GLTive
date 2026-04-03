# Purpose: Domain-level service exceptions for the stock module
"""
Stock Service Exceptions
Domain exceptions raised by stock business services.
These are NOT HTTP exceptions — the API layer maps them to responses.
"""


class StockServiceError(Exception):
    """Base exception for all stock service errors."""

    def __init__(self, message, code="stock_service_error", details=None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class StockNotFoundError(StockServiceError):
    """Raised when a requested stock entity does not exist within company scope."""

    def __init__(self, entity_type, entity_id):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(
            message=f"{entity_type} with id '{entity_id}' not found",
            code="stock_not_found",
            details={"entity_type": entity_type, "entity_id": str(entity_id)},
        )


class StockValidationError(StockServiceError):
    """Raised when a business validation rule is violated."""

    def __init__(self, message, field=None, details=None):
        self.field = field
        extra = details or {}
        if field:
            extra["field"] = field
        super().__init__(
            message=message,
            code="stock_validation_error",
            details=extra,
        )


class StockConflictError(StockServiceError):
    """Raised when a uniqueness or conflict constraint is violated."""

    def __init__(self, message, details=None):
        super().__init__(
            message=message,
            code="stock_conflict",
            details=details or {},
        )


class StockDeactivationBlockedError(StockServiceError):
    """Raised when deactivation is blocked by dependent active entities."""

    def __init__(self, entity_type, reason, blocking_count=0, details=None):
        self.entity_type = entity_type
        self.reason = reason
        self.blocking_count = blocking_count
        extra = details or {}
        extra.update({
            "entity_type": entity_type,
            "reason": reason,
            "blocking_count": blocking_count,
        })
        super().__init__(
            message=f"Cannot deactivate {entity_type}: {reason}",
            code="stock_deactivation_blocked",
            details=extra,
        )
