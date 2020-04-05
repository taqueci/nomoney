# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template
from django.utils.translation import gettext_lazy as _

from ..models import Account
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
        return 'badge badge-success'
    if category == journal.OUTGOING:
        return 'badge badge-danger'
    if category == journal.REPAYMENT:
        return 'badge badge-warning'

    return 'badge badge-secondary'


@register.filter
def journal_filter_items(request):
    item = []

    f_keyword = request.GET.get('keyword')
    f_start = request.GET.get('start')
    f_end = request.GET.get('end')
    f_debit = list(request.GET.getlist('debit'))
    f_credit = list(request.GET.getlist('credit'))

    if f_keyword:
        item.append({'key': _('Keyword'), 'value': f_keyword})

    if f_start:
        item.append({'key': _('Start date'), 'value': f_start})

    if f_end:
        item.append({'key': _('End date'), 'value': f_end})

    if f_debit:
        for x in Account.objects.filter(id__in=f_debit):
            item.append({'key': _('Debit'), 'value': x.name})

    if f_credit:
        for x in Account.objects.filter(id__in=f_credit):
            item.append({'key': _('Credit'), 'value': x.name})

    return item
