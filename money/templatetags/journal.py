# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template
from django.utils.translation import gettext_lazy as _

from ..models import Account, Tag
from ..views.shared import journal

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
    items = []

    f_keyword = request.GET.get('keyword')
    f_start = request.GET.get('start')
    f_end = request.GET.get('end')
    f_entries = request.GET.getlist('entry')
    f_debits = request.GET.getlist('debit')
    f_credits = request.GET.getlist('credit')
    f_max = request.GET.get('max')
    f_min = request.GET.get('min')
    f_tags = request.GET.getlist('tag')

    if f_keyword:
        items.append({'key': _('Keyword'), 'value': f_keyword})

    if f_start:
        items.append({'key': _('Start date'), 'value': f_start})

    if f_end:
        items.append({'key': _('End date'), 'value': f_end})

    for x in f_entries:
        label_d = Account.Entry(int(int(x) / 10)).label
        label_c = Account.Entry(int(x) % 10).label

        items.append({'key': _('Entry'), 'value': f'{label_d} / {label_c}'})

    for x in Account.objects.filter(id__in=f_debits):
        items.append({'key': _('Debit'), 'value': x.name})

    for x in Account.objects.filter(id__in=f_credits):
        items.append({'key': _('Credit'), 'value': x.name})

    if f_max and f_max.isdecimal():
        items.append({
            'key': _('Max amount'), 'value': f'{int(f_max):,}'
        })

    if f_min and f_min.isdecimal():
        items.append({
            'key': _('Min amount'), 'value': f'{int(f_min):,}'
        })

    for x in Tag.objects.filter(id__in=f_tags):
        items.append({'key': _('Tag'), 'value': x.name})

    return items
