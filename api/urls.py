# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL configuration for API."""

from django.urls import path

from .views import attachments, journals

app_name = 'api'

urlpatterns = [
    path('attachments', attachments.List.as_view(), name='attachments'),
    path('journals/export', journals.Export.as_view(), name='journals_export'),
]
