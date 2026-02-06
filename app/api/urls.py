# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL configuration for API."""

from django.conf.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

from .views import accounts, attachments, journals, pages

app_name = 'api'

router = DefaultRouter()
router.register('accounts', accounts.AccountViewSet)
router.register('attachments', attachments.AttachmentViewSet)
router.register('journals', journals.JournalViewSet)
router.register('pages', pages.PageViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', include(router.urls)),
]
