# Copyright (C) Takeshi Nakamura. All rights reserved.

import datetime

from django.db.models import F, Sum
from django.shortcuts import render

from ..models import Account, Journal
from .shared import chart

INDEX_NUM = 5


def index(request):
    today = datetime.date.today()

    start = today.replace(month=1, day=1)
    end = today.replace(month=12, day=31)

    q = Journal.objects.filter(
        disabled=False, date__gte=start, date__lte=end
    )

    summary = q.aggregate(
        income=Sum('income'), expense=Sum('expense'),
        balance=Sum(F('income')-F('expense')),
    )

    outgoing = q.exclude(expense=0).values(
        'debit__id', 'debit__name'
    ).annotate(sum=Sum('expense')).order_by('-sum')

    return render(request, 'money/home/index.html', {
        'start': start, 'end':end,
        'page': q.order_by('-id')[:INDEX_NUM],
        'summary': summary, 'outgoing': outgoing,
        'data_doughnut_outgoing': chart.data_doughnut_outgoing(outgoing),
    })
