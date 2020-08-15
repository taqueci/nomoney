# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL Configuration"""

from django.contrib import admin
from django.urls import path, include

from .settings import DEBUG, URL_ROOT


urlpatterns = [
    path('{}admin/'.format(URL_ROOT), admin.site.urls),
    path('{}i18n/'.format(URL_ROOT), include('django.conf.urls.i18n')),
    path('{}system/'.format(URL_ROOT),
         include('system.urls', namespace='system')),
    path('{}money/'.format(URL_ROOT),
         include('money.urls', namespace='money')),
]

if DEBUG:
    from django.contrib.staticfiles.urls import static
    from .settings import MEDIA_URL, MEDIA_ROOT

    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
