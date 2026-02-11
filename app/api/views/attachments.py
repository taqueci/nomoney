# Copyright (C) Takeshi Nakamura. All rights reserved.

from django_filters import OrderingFilter, rest_framework as filters
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from money.views.shared.filters import AnyValuesMultipleFilter
from system.models import Attachment

from ..serializers import AttachmentSerializer, AttachmentUploadSerializer
from .shared.permission import HasPermission


class Filter(filters.FilterSet):
    author = AnyValuesMultipleFilter(field_name='author__username')

    o = OrderingFilter(
        fields=(
            ('id', 'id'),
            ('created', 'created'),
        )
    )

    class Meta:
        model = Attachment
        fields = {
            'digest': ['exact'],
            'created': ['gte', 'lte'],
        }


# pylint: disable-next=too-many-ancestors
class AttachmentViewSet(viewsets.ModelViewSet):
    filterset_class = Filter
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated & HasPermission]
    queryset = Attachment.objects.all().select_related()

    def get_serializer_class(self):
        match self.request.method:
            case 'POST':
                return AttachmentUploadSerializer

        return AttachmentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
