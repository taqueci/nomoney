# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL Configuration"""

from django.contrib import admin
from django.urls import include, path

from .settings import DEBUG, ROUTE_PREFIX

urlpatterns = [
    path(f'{ROUTE_PREFIX}/admin/', admin.site.urls),
    path(f'{ROUTE_PREFIX}/i18n/', include('django.conf.urls.i18n')),
    path(f'{ROUTE_PREFIX}/system/',
         include('system.urls', namespace='system')),
    path(f'{ROUTE_PREFIX}/doc/', include('doc.urls', namespace='doc')),
    path(f'{ROUTE_PREFIX}/money/', include('money.urls', namespace='money')),
    path(f'{ROUTE_PREFIX}/api/', include('api.urls', namespace='api')),
]

if DEBUG:
    from django.contrib.staticfiles.urls import static

    from .settings import MEDIA_ROOT, MEDIA_URL

    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

    import debug_toolbar  # pylint: disable=import-error

    urlpatterns += [
        path(f'{ROUTE_PREFIX}/__debug__/', include(debug_toolbar.urls)),
    ]
