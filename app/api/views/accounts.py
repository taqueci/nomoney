# Copyright (C) Takeshi Nakamura. All rights reserved.

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from money.models import Account
from money.views.shared.account import Filter

from ..serializers import (
    AccountDetailSerializer, AccountListSerializer, AccountSerializer,
)
from .shared.permission import HasPermission


# pylint: disable-next=too-many-ancestors
class AccountViewSet(viewsets.ModelViewSet):
    filterset_class = Filter
    permission_classes = [IsAuthenticated & HasPermission]
    queryset = Account.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return AccountListSerializer
            case 'retrieve':
                return AccountDetailSerializer

        return AccountSerializer
