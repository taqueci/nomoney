# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template

register = template.Library()


@register.filter
def value_percent(num, total):
    return 100 * num / total if total > 0 else 0


@register.simple_tag(takes_context=True)
def value_if_eq_query(context, key, val, value, default=''):
    vals = context['request'].GET.getlist(key)

    return value if str(val) in vals else default


@register.simple_tag
def value_if_eq(a, b, value, default=''):
    return value if a == b else default
