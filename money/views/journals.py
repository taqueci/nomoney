# Copyright (C) Takeshi Nakamura. All rights reserved.

import datetime

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from ..forms import JournalForm
from ..models import Account, Journal, Template
from .shared import account, pagination


INDEX_PER_PAGE = 20
INDEX_DEFAULT_SORT = '-date'
INDEX_SORTABLE_FIELDS = (
    'id', 'date', 'debit', 'credit', 'amount', 'summary',
)

POPULAR_ACCOUNT_NUM = 12

def index(request):
    n = request.GET.get('page')
    sort = request.GET.get('sort')
    order = request.GET.get('order')

    f_keyword = request.GET.get('keyword')

    f_start = request.GET.get('start')
    f_end = request.GET.get('end')

    f_debit = list(request.GET.getlist('debit'))
    f_credit = list(request.GET.getlist('credit'))

    account = Account.objects.all()

    q = Journal.objects.filter(disabled=False)

    if f_keyword:
        q = q.filter(
            Q(summary__contains=f_keyword) |
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

    if sort and (sort in INDEX_SORTABLE_FIELDS):
        q = q.order_by('-' + sort if order and (order == 'desc') else sort)
    else:
        q = q.order_by(INDEX_DEFAULT_SORT)

    paginator = Paginator(q, INDEX_PER_PAGE)
    page = pagination.page(paginator, n)

    return render(request, 'money/journals/index.html', {
        'page': page, 'total': paginator.count,
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

        return redirect(request.GET.get('next', 'money:journals'))

    v_template = request.GET.get('template')
    v_base = request.GET.get('base')

    grouped_account = account.grouped_objects()

    popular_account = Journal.objects.values(
        'debit__id', 'debit__name', 'credit__id', 'credit__name',
    ).annotate(
        debit_num=Count('debit__id'), credit_num=Count('credit__id')
    ).order_by('-debit_num', '-credit_num')[:POPULAR_ACCOUNT_NUM]

    template = Template.objects.filter(disabled=False).order_by('-rank')

    default = _template(v_template) if v_template else {
        'date': datetime.date.today()
    }

    if v_base:
        default = get_object_or_404(Journal, pk=v_base)
        default.date = datetime.date.today()

    return render(request, 'money/journals/new.html', {
        'object': default, 'template': template,
        'account': grouped_account, 'popular_account': popular_account,
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

        return redirect(request.GET.get('next', 'money:journals'))

    grouped_account = account.grouped_objects()

    popular_account = Journal.objects.values(
        'debit__id', 'debit__name', 'credit__id', 'credit__name',
    ).annotate(
        debit_num=Count('debit__id'), credit_num=Count('credit__id')
    ).order_by('-debit_num', '-credit_num')[:POPULAR_ACCOUNT_NUM]

    return render(request, 'money/journals/edit.html', {
        'object': obj,
        'account': grouped_account, 'popular_account': popular_account,
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

    return redirect('money:journals')


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


def _template(pk):
    obj = get_object_or_404(Template, pk=pk)

    obj.date = _template_date(obj.date)
    obj.summary = _template_text(obj.summary)
    obj.note = _template_text(obj.note)

    return obj


def _template_date(str):
    try:
        d = datetime.datetime.strptime(_template_text(str), '%Y-%m-%d').date()
    except ValueError:
        d = ''

    return d


def _template_text(text):
    if not text:
        return ''

    now = datetime.date.today()

    for x in (
        '%a', '%A', '%w', '%d', '%b', '%B', '%m', '%y', '%Y', '%j', '%U', '%W',
        '%c', '%x',
    ):
        text = text.replace(x, now.strftime(x))

    return text
