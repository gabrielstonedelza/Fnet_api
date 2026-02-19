"""
Account lockout middleware — Brute-force protection.

Tracks failed login attempts per IP+email and temporarily locks accounts
after too many failures.

Security+ alignment:
  - 1.0: Credential brute-force mitigation
  - 3.0: Defense in depth
  - 4.0: Account lockout implementation
"""

import time
import logging
from collections import defaultdict
from threading import Lock
from django.http import JsonResponse

logger = logging.getLogger(__name__)

# In-memory store (use Redis in production for multi-process)
_attempts: dict[str, list[float]] = defaultdict(list)
_lockouts: dict[str, float] = {}
_lock = Lock()

# Configuration
MAX_ATTEMPTS = 5          # Lock after 5 failed attempts
WINDOW_SECONDS = 300      # Within a 5-minute window
LOCKOUT_SECONDS = 900     # Lock for 15 minutes


class AccountLockoutMiddleware:
    """
    Blocks login requests from IPs that have exceeded the failure threshold.
    Only applies to the login endpoint.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to login endpoint
        if request.path.rstrip("/") != "/api/v1/auth/login" or request.method != "POST":
            return self.get_response(request)

        ip = self._get_ip(request)
        key = ip  # Could combine with email for per-user lockout

        # Check if currently locked out
        with _lock:
            lockout_until = _lockouts.get(key, 0)
            if time.time() < lockout_until:
                remaining = int(lockout_until - time.time())
                logger.warning("Blocked login attempt from locked IP: %s", ip)
                return JsonResponse(
                    {
                        "error": "Too many failed login attempts. Please try again later.",
                        "retry_after_seconds": remaining,
                    },
                    status=429,
                )

        response = self.get_response(request)

        # Track failed attempts (401 = wrong credentials)
        if response.status_code == 401:
            with _lock:
                now = time.time()
                # Clean old attempts outside the window
                _attempts[key] = [t for t in _attempts[key] if now - t < WINDOW_SECONDS]
                _attempts[key].append(now)

                if len(_attempts[key]) >= MAX_ATTEMPTS:
                    _lockouts[key] = now + LOCKOUT_SECONDS
                    _attempts[key] = []
                    logger.warning(
                        "Account locked for IP %s after %d failed attempts",
                        ip,
                        MAX_ATTEMPTS,
                    )

        elif response.status_code == 200:
            # Successful login — clear attempts
            with _lock:
                _attempts.pop(key, None)
                _lockouts.pop(key, None)

        return response

    @staticmethod
    def _get_ip(request) -> str:
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")
