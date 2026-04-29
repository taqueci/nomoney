# Copyright (C) Takeshi Nakamura. All rights reserved.

from itertools import groupby

from django_filters import OrderingFilter, rest_framework as filters

from money.models import Account, Journal

from .filters import AnyValuesMultipleFilter, KeywordFilter


def grouped_objects():
    accounts = Account.objects.all().order_by('entry', '-rank', 'name')
    grouped = groupby(accounts, key=lambda x: x.entry)
    entry_names = dict(Account.Entry.choices)

    return [{
        'entry': entry,
        'name': entry_names.get(entry),
        'data': list(group)
    } for entry, group in grouped]


def entry_sets():
    q = Journal.objects.values_list(
        'debit__entry', 'credit__entry'
    ).order_by(
        'debit__entry', 'credit__entry'
    ).distinct()

    return [{
        'value': Account.Entry(x[0]).value * 10 + Account.Entry(x[1]).value,
        'debit': Account.Entry(x[0]), 'credit': Account.Entry(x[1]),
    } for x in q]


class Filter(filters.FilterSet):
    entry = AnyValuesMultipleFilter()
    description = KeywordFilter()

    o = OrderingFilter(
        fields=(
            ('id', 'id'),
            ('name', 'name'),
            ('entry', 'entry'),
            ('rank', 'rank'),
            ('enabled', 'enabled'),
        )
    )

    class Meta:
        model = Account
        fields = ['name', 'enabled']
