# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL Configuration"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('system/', include('system.urls', namespace='system')),
    path('money/', include('money.urls', namespace='money')),
]
