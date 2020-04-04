# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.conf import settings


def site_values(request):
    return {
        'VERSION': settings.VERSION,
        'NAME': settings.NAME,
    }
