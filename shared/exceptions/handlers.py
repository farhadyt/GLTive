# Purpose: Custom DRF exception handler for consistent error response format
"""
GLTive Exception Handler
Produces error responses matching the platform's API error contract.
"""
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from modules.stock.services.exceptions import (
    StockServiceError,
    StockNotFoundError,
    StockValidationError,
    StockConflictError,
    StockDeactivationBlockedError,
)


# Mapping of stock domain exceptions to HTTP status codes
_STOCK_EXCEPTION_MAP = {
    StockNotFoundError: http_status.HTTP_404_NOT_FOUND,
    StockValidationError: http_status.HTTP_400_BAD_REQUEST,
    StockConflictError: http_status.HTTP_409_CONFLICT,
    StockDeactivationBlockedError: http_status.HTTP_409_CONFLICT,
}


def _build_stock_error_response(exc, status_code):
    """Build the platform error envelope for a stock domain exception."""
    field_errors = {}
    if isinstance(exc, StockValidationError) and exc.field:
        field_errors[exc.field] = [exc.message]

    return Response(
        {
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "field_errors": field_errors,
            },
        },
        status=status_code,
    )


def gltive_exception_handler(exc, context):
    """
    Custom exception handler that wraps DRF errors into the GLTive
    standard error response format:

    {
        "success": false,
        "error": {
            "code": "error_code",
            "message": "localization_key_or_detail",
            "details": {},
            "field_errors": {}
        }
    }
    """
    # Stock domain exceptions — catch BEFORE DRF handler
    if isinstance(exc, StockServiceError):
        status_code = _STOCK_EXCEPTION_MAP.get(
            type(exc), http_status.HTTP_400_BAD_REQUEST
        )
        return _build_stock_error_response(exc, status_code)

    response = exception_handler(exc, context)

    if response is None:
        return None

    error_data = {
        "success": False,
        "error": {
            "code": _get_error_code(exc, response),
            "message": _get_error_message(exc, response),
            "details": {},
            "field_errors": {},
        },
    }

    # Extract field-level validation errors safely
    if hasattr(response, "data") and isinstance(response.data, dict):
        field_errors = {}
        for field, errors in response.data.items():
            if field == "detail":
                continue
            try:
                field_errors[field] = (
                    errors if isinstance(errors, list) else [str(errors)]
                )
            except (TypeError, ValueError):
                field_errors[field] = [str(errors)]
        if field_errors:
            error_data["error"]["field_errors"] = field_errors

    response.data = error_data
    return response


def _get_error_code(exc, response):
    """Derive a stable error code from the exception."""
    if hasattr(exc, "default_code"):
        return exc.default_code
    status_map = {
        400: "validation_error",
        401: "authentication_failed",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
    }
    return status_map.get(response.status_code, "server_error")


def _get_error_message(exc, response):
    """Extract a human/localization-friendly message."""
    if hasattr(exc, "detail"):
        detail = exc.detail
        if isinstance(detail, str):
            return detail
        if isinstance(detail, list) and detail:
            return str(detail[0])
        if isinstance(detail, dict) and "detail" in detail:
            return str(detail["detail"])
    return str(exc)
