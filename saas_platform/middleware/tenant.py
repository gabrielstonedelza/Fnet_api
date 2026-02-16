"""
Tenant Context Middleware.

Attaches the user's active membership (and thus company) to every request.
All views can then access request.membership to scope queries.

The company is resolved from the X-Company-ID header or falls back to the
user's only active membership.
"""


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.membership = None
        request.company = None

        if request.user and request.user.is_authenticated:
            from accounts.models import Membership

            company_id = request.META.get("HTTP_X_COMPANY_ID")

            if company_id:
                try:
                    membership = Membership.objects.select_related(
                        "company", "company__subscription_plan", "branch"
                    ).get(
                        user=request.user, company_id=company_id, is_active=True,
                    )
                    request.membership = membership
                    request.company = membership.company
                except Membership.DoesNotExist:
                    pass
            else:
                memberships = Membership.objects.select_related(
                    "company", "company__subscription_plan", "branch"
                ).filter(user=request.user, is_active=True)

                if memberships.count() == 1:
                    request.membership = memberships.first()
                    request.company = request.membership.company

        response = self.get_response(request)
        return response
