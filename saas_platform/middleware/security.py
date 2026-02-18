"""
Merchant+ Security Headers Middleware

OWASP-aligned HTTP security headers for the Django API.
Covers CompTIA Security+ objectives:
  - 1.0: Threat mitigation (XSS, clickjacking, MIME sniffing)
  - 3.0: Architecture (defense in depth, least privilege)
  - 4.0: Implementation (secure protocols, header hardening)
"""


class SecurityHeadersMiddleware:
    """
    Adds security headers to every HTTP response.
    Should be placed early in the MIDDLEWARE stack, after SecurityMiddleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # -- Content-Type sniffing protection (OWASP A05:2021) --
        response["X-Content-Type-Options"] = "nosniff"

        # -- Clickjacking protection (OWASP A05:2021) --
        response["X-Frame-Options"] = "DENY"

        # -- Reflected XSS protection (legacy, but still useful) --
        response["X-XSS-Protection"] = "1; mode=block"

        # -- Referrer leak prevention --
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # -- Permissions Policy (disable unused browser APIs) --
        response["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), interest-cohort=()"
        )

        # -- Cache-Control for authenticated API responses --
        if request.user and request.user.is_authenticated:
            response["Cache-Control"] = (
                "no-store, no-cache, must-revalidate, private"
            )
            response["Pragma"] = "no-cache"

        # -- Cross-Origin isolation headers --
        response["Cross-Origin-Opener-Policy"] = "same-origin"
        response["Cross-Origin-Resource-Policy"] = "same-origin"

        return response
