# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def report_item_label(context, date):
    unit = context['request'].GET.get('unit', 'year')

    if unit == 'year':
        return date.year

    if unit == 'month':
        return date.strftime('%Y-%m')

    if unit == 'week':
        return date.strftime('%Y-W%W')

    return date.strftime('%Y-%m-%d')
