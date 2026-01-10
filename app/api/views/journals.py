# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework_csv import renderers

from money.models import Journal
from money.views.shared.journal import Filter

from ..serializers import (
    JournalDetailSerializer, JournalListSerializer, JournalSerializer,
)
from .shared.permission import HasPermission


class CsvRenderer(renderers.CSVRenderer):
    header = [
        'id', 'credit.entry.label', 'debit.entry.label', 'date', 'amount',
        'summary', 'fy', 'enabled', 'author.full_name', 'created', 'updated',
    ]

    labels = {
        'id': 'ID',
        'credit.entry.label': _('Credit'),
        'debit.entry.label': _('Debit'),
        'date': _('Date'),
        'amount': _('Amount'),
        'summary': _('Summary'),
        'fy': 'FY',
        'enabled': _('Enabled'),
        'author.full_name': _('Author'),
        'created': _('Created on'),
        'updated': _('Updated on'),
    }


# pylint: disable-next=too-many-ancestors
class JournalViewSet(viewsets.ModelViewSet):
    filterset_class = Filter
    permission_classes = [IsAuthenticated & HasPermission]
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [CsvRenderer]

    queryset = Journal.objects.all().select_related().prefetch_related(
        'tags', 'attachments',
    )

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return JournalListSerializer
            case 'retrieve':
                return JournalDetailSerializer

        return JournalSerializer

    def paginate_queryset(self, queryset):
        if self.request.accepted_renderer.format == CsvRenderer.format:
            return None

        return super().paginate_queryset(queryset)
