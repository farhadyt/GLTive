# Purpose: Development-specific Django settings for GLTive platform
"""
GLTive Platform — Development Settings
Extends base settings with debug-friendly configuration.
"""
from config.settings.base import *  # noqa: F401, F403

DEBUG = True

# ---------------------
# Debug toolbar
# ---------------------
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

INTERNAL_IPS = ["127.0.0.1"]

# ---------------------
# CORS — allow all in development
# ---------------------
CORS_ALLOW_ALL_ORIGINS = True

# ---------------------
# Email — console backend for development
# ---------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ---------------------
# Logging — verbose for development
# ---------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
