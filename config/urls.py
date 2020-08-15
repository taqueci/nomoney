# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL Configuration"""

from django.contrib import admin
from django.urls import path, include

from .settings import DEBUG, URL_ROOT


urlpatterns = [
    path(f'{URL_ROOT}admin/', admin.site.urls),
    path(f'{URL_ROOT}i18n/', include('django.conf.urls.i18n')),
    path(f'{URL_ROOT}system/', include('system.urls', namespace='system')),
    path(f'{URL_ROOT}money/', include('money.urls', namespace='money')),
]

if DEBUG:
    from django.contrib.staticfiles.urls import static
    from .settings import MEDIA_URL, MEDIA_ROOT

    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
