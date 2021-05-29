# Copyright (C) Takeshi Nakamura. All rights reserved.

import csv

from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import gettext as _

from rest_framework.views import APIView

from money.models import Journal


INDEX_DEFAULT_SORT = '-date'
INDEX_SORTABLE_FIELDS = (
    'id', 'date', 'debit', 'credit', 'amount', 'summary',
)


class Export(APIView):
    def get(self, request):
        query = _query(request)

        return _response_csv('journals.csv', query)


def _query(request):
    sort = request.GET.get('sort')
    order = request.GET.get('order')

    f_keyword = request.GET.get('keyword')

    f_start = request.GET.get('start')
    f_end = request.GET.get('end')

    f_debit = list(request.GET.getlist('debit'))
    f_credit = list(request.GET.getlist('credit'))

    f_max = request.GET.get('max')
    f_min = request.GET.get('min')

    f_tag = list(request.GET.getlist('tag'))

    q = Journal.objects.filter(disabled=False)

    if f_keyword:
        q = q.filter(
            Q(summary__icontains=f_keyword) |
            Q(note__icontains=f_keyword)
        )

    if f_start:
        q = q.filter(date__gte=f_start)

    if f_end:
        q = q.filter(date__lte=f_end)

    if f_debit:
        q = q.filter(debit__in=f_debit)

    if f_credit:
        q = q.filter(credit__in=f_credit)

    if f_min and f_min.isdecimal():
        q = q.filter(amount__gte=f_min)

    if f_max and f_max.isdecimal():
        q = q.filter(amount__lte=f_max)

    if f_tag:
        q = q.filter(tags__in=f_tag)

    if sort and (sort in INDEX_SORTABLE_FIELDS):
        q = q.order_by('-' + sort if order and (order == 'desc') else sort)
    else:
        q = q.order_by(INDEX_DEFAULT_SORT)

    return q.select_related('debit', 'credit')


def _response_csv(name, query):
    r = HttpResponse(content_type='text/csv')
    r['Content-Disposition'] = f'attachment; filename="{name}"'

    w = csv.writer(r)
    w.writerow([
        '#', _('Date'), _('Debit'), _('Credit'), _('Amount'), _('Summary'),
        _('Note'),
    ])

    for x in query:
        w.writerow([
            x.pk, x.date, x.debit.name, x.credit.name, x.amount, x.summary,
            x.note,
        ])

    return r
