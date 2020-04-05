# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template
from django.utils.translation import gettext_lazy as _

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
