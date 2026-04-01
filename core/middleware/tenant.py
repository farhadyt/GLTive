# Purpose: Tenant resolution middleware placeholder for company-scoped request context
"""
GLTive Tenant Middleware
Resolves current tenant/company from the authenticated user's context
and attaches it to the request for downstream use.

TODO: Implement tenant resolution:
- Extract company from authenticated user
- Attach request.company for use in views and services
- Handle vendor admin vs company admin context
- Enforce tenant isolation at middleware level
"""


class TenantMiddleware:
    """
    Middleware to resolve and attach the current company context to each request.

    Usage:
        After implementation, add to MIDDLEWARE in settings:
        'core.middleware.tenant.TenantMiddleware'
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # TODO: Resolve company from authenticated user
        # request.company = resolve_company(request.user)
        response = self.get_response(request)
        return response
