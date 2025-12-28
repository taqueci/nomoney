# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL configuration for API."""

from django.conf.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from rest_framework.routers import DefaultRouter

from .views import accounts, attachments, journals

app_name = 'api'

router = DefaultRouter()
router.register('accounts', accounts.AccountViewSet)
router.register('journals', journals.JournalViewSet)

urlpatterns = [
    path('attachments', attachments.List.as_view(), name='attachments'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', include(router.urls)),
]
