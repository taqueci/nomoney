# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.core.paginator import Paginator
from django.shortcuts import render

from ..models import Journal
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

    q = Journal.objects.filter(disabled=False)

    if sort and (sort in INDEX_SORTABLE_FIELDS):
        q = q.order_by('-' + sort if order and (order == 'desc') else sort)
    else:
        q = q.order_by(INDEX_DEFAULT_SORT)

    paginator = Paginator(q, INDEX_PER_PAGE)
    page = pagination.page(paginator, n)

    return render(request, 'money/journals/index.html', {
        'page': page
    })
