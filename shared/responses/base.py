# Purpose: Standard API response wrappers matching GLTive response contract
"""
GLTive Standard Responses
Helper functions for consistent API response format.
"""
from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message=None, http_status=status.HTTP_200_OK, meta=None):
    """
    Standard success response:
    {
        "success": true,
        "message": "optional_key",
        "data": {},
        "meta": {}
    }
    """
    payload = {"success": True}
    if message:
        payload["message"] = message
    if data is not None:
        payload["data"] = data
    if meta:
        payload["meta"] = meta
    return Response(payload, status=http_status)


def created_response(data=None, message=None):
    """Shorthand for 201 Created responses."""
    return success_response(data=data, message=message, http_status=status.HTTP_201_CREATED)
