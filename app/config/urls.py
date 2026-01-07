# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL Configuration"""

from django.contrib import admin
from django.urls import include, path

from .settings import DEBUG, ROUTE_PREFIX

sub_url_patterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('system/', include('system.urls', namespace='system')),
    path('doc/', include('doc.urls', namespace='doc')),
    path('money/', include('money.urls', namespace='money')),
    path('api/', include('api.urls', namespace='api')),
]

urlpatterns = [
    path(f'{ROUTE_PREFIX}/', include(sub_url_patterns)),
]

if DEBUG:
    from django.contrib.staticfiles.urls import static

    from .settings import MEDIA_ROOT, MEDIA_URL

    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

    import debug_toolbar  # pylint: disable=import-error

    sub_url_patterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
