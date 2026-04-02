# Purpose: Evaluates company context for each authenticated request
"""
GLTive Tenant Middleware
Extracts company context from an authenticated user and attaches it directly
to the request object for safe usage within views and serializers.
"""
from django.utils.deprecation import MiddlewareMixin


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware that ensures request.company is always populated consistently.
    If the request has an authenticated user attached to a company, request.company = user.company.
    Otherwise, request.company is explicitly None.
    
    This middleware never throws 403s itself; it simply populates context 
    and leaves access control to permission classes.
    """

    def process_request(self, request):
        # Default state
        request.company = None

        if hasattr(request, "user") and request.user.is_authenticated:
            # If the user has an attached company (standard case)
            if hasattr(request.user, "company") and request.user.company:
                request.company = request.user.company
