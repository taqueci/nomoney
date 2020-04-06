# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.db.models import F, Sum
from django.shortcuts import render

from ..models import Journal
from .shared import chart, date, value

INDEX_NUM = 7


def index(request):
    q = Journal.objects.filter(disabled=False)

    annual = q.values('year').annotate(
        income=Sum('income'), expense=Sum('expense'),
        balance=F('income')-F('expense')
    ).order_by('-year')[:INDEX_NUM]

    monthly = q.values('year', 'month').annotate(
        income=Sum('income'), expense=Sum('expense'),
        balance=F('income')-F('expense')
    ).order_by('-year', '-month')[:INDEX_NUM]

    weekly = q.values('year', 'month', 'week').annotate(
        income=Sum('income'), expense=Sum('expense'),
        balance=F('income')-F('expense')
    ).order_by('-year', '-month', '-week')[:INDEX_NUM]

    daily = q.values('date').annotate(
        income=Sum('income'), expense=Sum('expense'),
        balance=F('income')-F('expense')
    ).order_by('-date')[:INDEX_NUM]

    return render(request, 'money/reports/index.html', {
        'annual': annual, 'monthly': monthly, 'weekly': weekly, 'daily': daily,
    })


def show(request, id):
    q = Journal.objects.filter(disabled=False)

    f_start = request.GET.get('start', '1970-01-01')
    f_end = request.GET.get('end', '2100-12-31')

    if f_start:
        q = q.filter(date__gte=f_start)

    if f_end:
        q = q.filter(date__lte=f_end)

    summary = q.aggregate(
        income=Sum('income'), expense=Sum('expense'),
        asset=Sum('asset'), liability=Sum('liability'), equity=Sum('equity'),
        balance=Sum(F('income')-F('expense')),
        net=Sum(F('asset')-F('liability')),
    )

    incoming = q.exclude(income=0).values(
        'credit__id', 'credit__name'
    ).annotate(sum=Sum('income')).order_by('-sum')

    outgoing = q.exclude(expense=0).values(
        'debit__id', 'debit__name'
    ).annotate(sum=Sum('expense')).order_by('-sum')

    return render(request, 'money/reports/show.html', {
        'page': date.range_next_prev(f_start, f_end),
        'summary': summary, 'incoming': incoming, 'outgoing': outgoing,
        'data_doughnut_incoming': chart.data_doughnut_incoming(incoming),
        'data_doughnut_outgoing': chart.data_doughnut_outgoing(outgoing),
    })
