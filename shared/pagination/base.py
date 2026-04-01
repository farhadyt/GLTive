# Purpose: Standard pagination class matching GLTive API contract
"""
GLTive Standard Pagination
Matches the pagination format defined in the API contract.
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """
    Platform-wide pagination following the GLTive API contract:

    {
        "success": true,
        "data": {
            "items": [...],
            "pagination": {
                "page": 1,
                "page_size": 20,
                "total_items": 140,
                "total_pages": 7
            }
        }
    }
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "success": True,
                "data": {
                    "items": data,
                    "pagination": {
                        "page": self.page.number,
                        "page_size": self.get_page_size(self.request),
                        "total_items": self.page.paginator.count,
                        "total_pages": self.page.paginator.num_pages,
                    },
                },
            }
        )
