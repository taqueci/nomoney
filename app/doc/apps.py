# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Application configuration for document."""

from django.apps import AppConfig


class DocConfig(AppConfig):
    """Metadata for document application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doc'
