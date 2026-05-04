# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Application configuration for system."""

from django.apps import AppConfig


class SystemConfig(AppConfig):
    """Metadata for system."""

    name = 'system'

    def ready(self):
        # pylint: disable-next=import-outside-toplevel,unused-import
        from . import signals
