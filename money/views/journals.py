# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.core.paginator import Paginator
from django.shortcuts import render

from ..models import Account, Journal
from .shared import pagination


INDEX_PER_PAGE = 20
INDEX_DEFAULT_SORT = '-date'
INDEX_SORTABLE_FIELDS = (
    'id', 'date', 'debit', 'credit', 'amount', 'summary',
)


def index(request):
    n = request.GET.get('page')
    sort = request.GET.get('sort')
    order = request.GET.get('order')

    f_start = request.GET.get('start')
    f_end = request.GET.get('end')

    f_debit = list(request.GET.getlist('debit'))
    f_credit = list(request.GET.getlist('credit'))

    account = Account.objects.all()

    q = Journal.objects.filter(disabled=False)

    if f_start:
        q = q.filter(date__gte=f_start)

    if f_end:
        q = q.filter(date__lte=f_end)

    if f_debit:
        q = q.filter(debit__in=f_debit)

    if f_credit:
        q = q.filter(credit__in=f_credit)

    if sort and (sort in INDEX_SORTABLE_FIELDS):
        q = q.order_by('-' + sort if order and (order == 'desc') else sort)
    else:
        q = q.order_by(INDEX_DEFAULT_SORT)

    paginator = Paginator(q, INDEX_PER_PAGE)
    page = pagination.page(paginator, n)

    return render(request, 'money/journals/index.html', {
        'page': page,
        'debit': account, 'credit': account,
    })
