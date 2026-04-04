# Purpose: Production-specific Django settings for GLTive platform
"""
GLTive Platform — Production Settings
Extends base settings with security-hardened configuration.
Production startup fails explicitly if critical secrets are missing.
"""
import os

from config.settings.base import *  # noqa: F401, F403

DEBUG = False

# ---------------------
# Production secret enforcement
# ---------------------
if not SECRET_KEY:  # noqa: F405
    raise RuntimeError(
        "DJANGO_SECRET_KEY environment variable is required in production. "
        "Generate a strong key (minimum 50 characters) and set it in your environment."
    )

if len(SECRET_KEY) < 32:  # noqa: F405
    raise RuntimeError(
        "DJANGO_SECRET_KEY is too short for production. "
        "Use at least 50 characters for cryptographic safety."
    )

# ---------------------
# Security hardening
# ---------------------
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() == "true"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# ---------------------
# CORS — strict in production
# ---------------------
CORS_ALLOW_ALL_ORIGINS = False
_cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in _cors_origins.split(",") if origin.strip()
]

# ---------------------
# Logging — structured for production
# ---------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "structured": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "structured",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "modules.stock": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
