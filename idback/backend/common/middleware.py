"""
Security middleware for the MERIDIAN API.
"""

import time
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.sites.models import Site


def _get_site_settings():
    """Get SiteSettings with fallback defaults."""
    try:
        from common.models import SiteSettings

        site = Site.objects.get_current()
        settings_obj, _ = SiteSettings.objects.get_or_create(site=site, defaults={})
        return settings_obj
    except Exception:
        return None


class RateLimitMiddleware:
    """
    Rate limiting middleware using Redis cache.
    Config loaded from SiteSettings.rate_limit_config.
    """

    # Map URL patterns to config keys
    RATE_LIMIT_RULES = [
        ("/api/v1/auth/login/", "login"),
        ("/api/v1/auth/register/", "register"),
        ("/api/v1/auth/verify/", "otp"),
        ("/api/v1/auth/resend-verification/", "otp"),
        ("/api/v1/auth/forgot-password/", "otp"),
        ("/api/v1/auth/reset-password/", "otp"),
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only rate limit POST requests to matched paths
        if request.method == "POST":
            path = request.path
            for pattern, config_key in self.RATE_LIMIT_RULES:
                if path.startswith(pattern):
                    self._check_rate_limit(request, config_key)
                    break

        response = self.get_response(request)
        return response

    def _check_rate_limit(self, request, config_key):
        """Check rate limit for a given config key. Raises 429 if exceeded."""
        site_settings = _get_site_settings()

        # Get limits from site config or use defaults
        defaults = {
            "login": {"max_attempts": 5, "window_seconds": 60},
            "register": {"max_attempts": 3, "window_seconds": 3600},
            "api": {"max_requests": 100, "window_seconds": 60},
            "otp": {"max_attempts": 5, "window_seconds": 300},
        }

        if site_settings and site_settings.rate_limit_config:
            limits = {**defaults}
            limits.update(site_settings.rate_limit_config)
        else:
            limits = defaults

        rule = limits.get(
            config_key, limits.get("api", {"max_attempts": 100, "window_seconds": 60})
        )
        max_attempts = rule.get("max_attempts", 100)
        window = rule.get("window_seconds", 60)

        # Use IP address as identifier
        ip = self._get_client_ip(request)
        cache_key = f"rl:{config_key}:{ip}"

        current = cache.get_or_set(cache_key, 0, window)
        if current >= max_attempts:
            from ninja.errors import HttpError

            raise HttpError(429, "Too many attempts. Please try again later.")

        cache.incr(cache_key)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")


class AdminIPRestrictionMiddleware:
    """
    Restricts Django admin access to allowed IPs.
    Config loaded from SiteSettings.security_config.admin_allowed_ips.
    Only active when DEBUG=False.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG and request.path.startswith("/admin/"):
            self._check_admin_access(request)
        return self.get_response(request)

    def _check_admin_access(self, request):
        site_settings = _get_site_settings()
        allowed_ips = []

        if site_settings and site_settings.security_config:
            allowed_ips = site_settings.security_config.get("admin_allowed_ips", [])

        # If no IPs configured, allow all (admin must configure this)
        if not allowed_ips:
            return

        ip = request.META.get("REMOTE_ADDR", "")
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()

        if ip not in allowed_ips:
            from django.http import HttpResponseForbidden

            raise HttpResponseForbidden("Access denied")


class RequestLoggingMiddleware:
    """
    Logs API requests for security auditing.
    Logs method, path, status code, IP, and user (if authenticated).
    """

    # Paths to skip logging (health checks, static, media)
    SKIP_PATHS = ("/static/", "/media/", "/admin/login/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip non-API and static paths
        if not request.path.startswith("/api/v1/"):
            return self.get_response(request)

        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        # Log the request
        self._log_request(request, response, duration)

        return response

    def _log_request(self, request, response, duration):
        import logging

        logger = logging.getLogger("api.access")

        user_info = "anonymous"
        if hasattr(request, "auth") and request.auth:
            user_info = str(request.auth)
        elif request.user and request.user.is_authenticated:
            user_info = request.user.username

        ip = request.META.get("REMOTE_ADDR", "unknown")

        logger.info(
            f"{request.method} {request.path} -> {response.status_code} "
            f"[{ip}] user={user_info} {duration:.3f}s"
        )
