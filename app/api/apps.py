# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Application configuration for API."""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Metadata for API."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
