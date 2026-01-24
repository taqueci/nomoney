# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework_csv import renderers

from doc.models import Page
from doc.views import PageFilter

from ..serializers import (
    PageDetailSerializer, PageListSerializer, PageSerializer,
)
from .shared.permission import HasPermission


# pylint: disable-next=too-many-ancestors
class PageViewSet(viewsets.ModelViewSet):
    filterset_class = PageFilter
    permission_classes = [IsAuthenticated & HasPermission]

    queryset = Page.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return PageListSerializer
            case 'retrieve':
                return PageDetailSerializer

        return PageSerializer
