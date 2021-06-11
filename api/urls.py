# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL configuration for API."""

from django.urls import path

from .views import journals


app_name = 'api'

urlpatterns = [
    path('journals/export', journals.Export.as_view(), name='journals_export'),
]
