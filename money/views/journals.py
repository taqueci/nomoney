# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from ..forms import JournalForm
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


def new(request):
    if request.method == 'POST':
        if create(request):
            messages.success(
                request, _('New journal has been successfully created')
            )
        else:
            messages.error(request, _('Failed to create journal'))

        return redirect(request.GET.get('next', 'main:journals'))

    account = Account.objects.all()

    return render(request, 'money/journals/new.html', {
        'debit': account, 'credit': account,
    })


def show(request, id):
    obj = get_object_or_404(Journal, pk=id)

    return render(request, 'money/journals/show.html', {
        'object': obj
    })


def edit(request, id):
    obj = get_object_or_404(Journal, pk=id)

    if request.method == 'POST':
        if update(request, obj):
            messages.success(
                request, _('The journal has been successfully updated')
            )
        else:
            messages.error(request, _('Failed to update journal'))

        return redirect(request.GET.get('next', 'main:journals'))

    account = Account.objects.all()

    return render(request, 'money/journals/edit.html', {
        'object': obj,
        'debit': account, 'credit': account,
    })


def destroy(request, id):
    obj = get_object_or_404(Journal, pk=id)

    if request.method == 'POST':
        if delete(request, obj):
            messages.success(
                request, _('The journal has been successfully deleted')
            )
        else:
            messages.error(request, _('Failed to delete journal'))

    return redirect('main:journals')


def create(request):
    form = JournalForm(request.POST)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()

        return True

    return False


def update(request, obj):
    form = JournalForm(request.POST, instance=obj)

    if form.is_valid():
        form.save()

        return True

    return False


def delete(request, obj):
    obj.disabled = True
    obj.save()

    return True
