# Purpose: Custom DRF exception handler for consistent error response format
"""
GLTive Exception Handler
Produces error responses matching the platform's API error contract.
"""
from rest_framework.views import exception_handler


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
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            "success": False,
            "error": {
                "code": _get_error_code(exc, response),
                "message": _get_error_message(exc, response),
                "details": {},
                "field_errors": {},
            },
        }

        # Extract field-level validation errors
        if hasattr(response, "data") and isinstance(response.data, dict):
            field_errors = {}
            for field, errors in response.data.items():
                if field != "detail":
                    field_errors[field] = (
                        errors if isinstance(errors, list) else [str(errors)]
                    )
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
    return str(exc)
