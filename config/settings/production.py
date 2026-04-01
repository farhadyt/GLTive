# Purpose: Production-specific Django settings for GLTive platform
"""
GLTive Platform — Production Settings
Extends base settings with security-hardened configuration.
"""
from config.settings.base import *  # noqa: F401, F403

DEBUG = False

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

# ---------------------
# CORS — restrict in production
# ---------------------
CORS_ALLOW_ALL_ORIGINS = False
# TODO: Set CORS_ALLOWED_ORIGINS from environment variable

# ---------------------
# Logging — structured for production
# ---------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
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
    },
}
