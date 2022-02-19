# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template
from django.utils.translation import gettext_lazy as _

from money.models import Account, Tag
from money.views.shared import journal

register = template.Library()


@register.filter
def journal_category_text(obj):
    category = journal.category(obj)

    if category == journal.INCOMING:
        return _('Incoming')
    if category == journal.OUTGOING:
        return _('Outgoing')
    if category == journal.REPAYMENT:
        return _('Repayment')

    return _('Other')


@register.filter
def journal_category_badge_class(obj):
    category = journal.category(obj)

    if category == journal.INCOMING:
        return 'badge bg-success'
    if category == journal.OUTGOING:
        return 'badge bg-danger'
    if category == journal.REPAYMENT:
        return 'badge bg-warning'

    return 'badge bg-secondary'


@register.filter
def journal_html_selected_if_has_tag(obj, tag):
    if hasattr(obj, 'tags') and tag.id in [x.id for x in obj.tags.all()]:
        return 'selected'

    return ''


@register.filter
def journal_filter_items(request):
    item = []

    f_keyword = request.GET.get('keyword')
    f_start = request.GET.get('start')
    f_end = request.GET.get('end')
    f_entry = list(request.GET.getlist('entry'))
    f_debit = list(request.GET.getlist('debit'))
    f_credit = list(request.GET.getlist('credit'))
    f_max = request.GET.get('max')
    f_min = request.GET.get('min')
    f_tag = list(request.GET.getlist('tag'))

    if f_keyword:
        item.append({'key': _('Keyword'), 'value': f_keyword})

    if f_start:
        item.append({'key': _('Start date'), 'value': f_start})

    if f_end:
        item.append({'key': _('End date'), 'value': f_end})

    if f_entry:
        for x in f_entry:
            label_d = Account.Entry(int(int(x) / 10)).label
            label_c = Account.Entry(int(x) % 10).label

            item.append({'key': _('Entry'), 'value': f'{label_d} / {label_c}'})

    if f_debit:
        for x in Account.objects.filter(id__in=f_debit):
            item.append({'key': _('Debit'), 'value': x.name})

    if f_credit:
        for x in Account.objects.filter(id__in=f_credit):
            item.append({'key': _('Credit'), 'value': x.name})

    if f_max and f_max.isdecimal():
        item.append({
            'key': _('Max amount'), 'value': f'{int(f_max):,}'
        })

    if f_min and f_min.isdecimal():
        item.append({
            'key': _('Min amount'), 'value': f'{int(f_min):,}'
        })

    if f_tag:
        for x in Tag.objects.filter(id__in=f_tag):
            item.append({'key': _('Tag'), 'value': x.name})

    return item
