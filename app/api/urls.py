# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL configuration for API."""

from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import attachments, journals

app_name = 'api'

router = DefaultRouter()
router.register('journals', journals.JournalViewSet)

urlpatterns = [
    path('attachments', attachments.List.as_view(), name='attachments'),
    path('journals/export', journals.Export.as_view(), name='journals_export'),
    path('', include(router.urls)),
]
