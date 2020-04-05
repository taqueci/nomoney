# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template
from django.utils.translation import gettext_lazy as _

from ..models import Account

register = template.Library()


@register.filter
def journal_category_text(obj):
    if obj.credit.entry == Account.ENTRY_INCOME:
        return _('Incoming')
    if obj.debit.entry == Account.ENTRY_EXPENSE:
        return _('Outgoing')
    if obj.debit.entry == Account.ENTRY_LIABILITY:
        return _('Repayment')
    
    return _('Other')


@register.filter
def journal_category_badge_class(obj):
    if obj.credit.entry == Account.ENTRY_INCOME:
        return 'badge badge-success'
    if obj.debit.entry == Account.ENTRY_EXPENSE:
        return 'badge badge-danger'
    if obj.debit.entry == Account.ENTRY_LIABILITY:
        return 'badge badge-warning'
    
    return 'badge badge-secondary'

