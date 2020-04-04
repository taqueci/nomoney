# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL Configuration"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('money/', include('money.urls', namespace='money')),
]
