# Copyright (C) Takeshi Nakamura. All rights reserved.

import csv

from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import gettext as _

from rest_framework.views import APIView

from money.models import Journal
from money.views.journals import IndexFilter


INDEX_DEFAULT_SORT = '-date'


class Export(APIView):
    def get(self, request):
        query = _query(request)

        return _response_csv('journals.csv', query)


def _query(request):
    q = Journal.objects.filter(disabled=False).order_by(INDEX_DEFAULT_SORT)

    f_keyword = request.GET.get('keyword')

    if f_keyword:
        q = q.filter(
            Q(summary__icontains=f_keyword) |
            Q(note__icontains=f_keyword)
        )

    return IndexFilter(request.GET, queryset=q).qs.select_related()


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
