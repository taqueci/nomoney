# Copyright (C) Takeshi Nakamura. All rights reserved.

from functools import reduce

import django_filters
from django.db.models import Q
from django_filters import (
    AllValuesMultipleFilter, DateFilter, NumberFilter, OrderingFilter,
)

from money.models import Account, Journal

from .filters import AnyValuesMultipleFilter

UNDEFINED = 0
INCOMING = 1
OUTGOING = 2
REPAYMENT = 3


def category(obj):
    if obj.credit.entry == Account.Entry.INCOME:
        return INCOMING
    if obj.debit.entry == Account.Entry.EXPENSE:
        return OUTGOING
    if obj.debit.entry == Account.Entry.LIABILITY:
        return REPAYMENT

    return UNDEFINED


class KeywordFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        for x in value.split():
            qs = qs.filter(Q(summary__icontains=x) | Q(note__icontains=x))

        return qs


class EntryFilter(AnyValuesMultipleFilter):
    def filter(self, qs, value):
        if not value:
            return qs

        params = []

        for x in value:
            entry_d = int(int(x) / 10)
            entry_c = int(x) % 10

            params.append(Q(debit__entry=entry_d, credit__entry=entry_c))

        return qs.filter(reduce(lambda x, y: x | y, params))


class Filter(django_filters.FilterSet):
    debit = AllValuesMultipleFilter(field_name='debit_id')
    credit = AllValuesMultipleFilter(field_name='credit_id')

    start = DateFilter(field_name='date', lookup_expr='gte')
    end = DateFilter(field_name='date', lookup_expr='lte')

    min = NumberFilter(field_name='amount', lookup_expr='gte')
    max = NumberFilter(field_name='amount', lookup_expr='lte')

    tag = AllValuesMultipleFilter(field_name='tags')

    keyword = KeywordFilter()
    entry = EntryFilter()

    sort = OrderingFilter(
        fields=(
            ('id', 'id'), ('date', 'date'),
            ('debit', 'debit'), ('credit', 'credit'),
            ('amount', 'amount'), ('summary', 'summary'),
        )
    )

    class Meta:
        model = Journal
        exclude = ('created', 'updated')
