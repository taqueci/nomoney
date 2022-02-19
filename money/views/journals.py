# Copyright (C) Takeshi Nakamura. All rights reserved.

import datetime
from functools import reduce

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django_filters import (
    AllValuesMultipleFilter, CharFilter, DateFilter, FilterSet, NumberFilter,
    OrderingFilter,
)

from money.forms import JournalForm
from money.models import Journal, Tag, Template
from money.views.shared import account, pagination
from money.views.shared.filters import AnyValuesMultipleFilter

INDEX_PER_PAGE = 20
INDEX_DEFAULT_SORT = '-date'

POPULAR_ACCOUNT_NUM = 12


class KeywordFilter(CharFilter):
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


class IndexFilter(FilterSet):
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


def index(request):
    n = request.GET.get('page')

    q = Journal.objects.available().order_by(INDEX_DEFAULT_SORT)
    q = IndexFilter(request.GET, queryset=q).qs

    # For performance improvement
    q = q.select_related().prefetch_related('tags')

    tags = Tag.objects.all()
    entry_sets = account.entry_sets()
    grouped_accounts = account.grouped_objects()

    paginator = Paginator(q, INDEX_PER_PAGE)

    return render(request, 'money/journals/index.html', {
        'page': pagination.page(paginator, n), 'total': paginator.count,
        'entry_sets': entry_sets, 'accounts': grouped_accounts, 'tags': tags,
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

    tags = Tag.objects.all()
    grouped_accounts = account.grouped_objects()

    popular_accounts = Journal.objects.values(
        'debit__id', 'debit__name', 'credit__id', 'credit__name',
    ).annotate(
        debit_num=Count('debit__id'), credit_num=Count('credit__id')
    ).order_by('-debit_num', '-credit_num')[:POPULAR_ACCOUNT_NUM]

    templates = Template.objects.available().order_by('-rank')

    default = _template(v_template) if v_template else {
        'date': datetime.date.today()
    }

    if v_base:
        default = get_object_or_404(Journal, pk=v_base)
        default.date = datetime.date.today()

    return render(request, 'money/journals/new.html', {
        'object': default, 'templates': templates, 'tags': tags,
        'accounts': grouped_accounts, 'popular_accounts': popular_accounts,
    })


def show(request, pk):
    obj = get_object_or_404(Journal, pk=pk)

    return render(request, 'money/journals/show.html', {
        'object': obj
    })


def edit(request, pk):
    obj = get_object_or_404(Journal, pk=pk)

    if request.method == 'POST':
        if update(request, obj):
            messages.success(
                request, _('The journal has been successfully updated')
            )
        else:
            messages.error(request, _('Failed to update journal'))

        return redirect(request.GET.get('next', 'money:journals'))

    tags = Tag.objects.all()
    grouped_accounts = account.grouped_objects()

    popular_accounts = Journal.objects.values(
        'debit__id', 'debit__name', 'credit__id', 'credit__name',
    ).annotate(
        debit_num=Count('debit__id'), credit_num=Count('credit__id')
    ).order_by('-debit_num', '-credit_num')[:POPULAR_ACCOUNT_NUM]

    return render(request, 'money/journals/edit.html', {
        'object': obj, 'tags': tags,
        'accounts': grouped_accounts, 'popular_accounts': popular_accounts,
    })


def destroy(request, pk):
    obj = get_object_or_404(Journal, pk=pk)

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
        form.save_m2m()

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


def _template_date(s):
    try:
        d = datetime.datetime.strptime(_template_text(s), '%Y-%m-%d').date()
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
