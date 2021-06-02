# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Context processors."""

from django.conf import settings


def site_values(request):
    """Enable using global constants for templates."""

    return {
        'VERSION': settings.VERSION,
        'NAME': settings.NAME,
    }
