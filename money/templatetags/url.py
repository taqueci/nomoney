# Copyright (C) Takeshi Nakamura. All rights reserved.

import re

from django import template

from money.views.shared import date

register = template.Library()


@register.simple_tag(takes_context=True)
def url_param_value(context, key):
    return context['request'].GET.get(key, '')


@register.simple_tag(takes_context=True)
def url_params(context, **kwargs):
    query = context['request'].GET.copy()

    for key, val in kwargs.items():
        query[key] = val

    return query.urlencode()


@register.simple_tag(takes_context=True)
def url_params_sort(context, key):
    query = context['request'].GET.copy()

    sort = context['request'].GET.get('sort', '')

    (order, field) = re.match(r'(-?)(.*)', sort).groups()

    if (key == field) and (order == ''):
        query['sort'] = f'-{key}'
    else:
        query['sort'] = key

    return query.urlencode()


@register.simple_tag(takes_context=True)
def url_params_period(context, **kwargs):
    query = context['request'].GET.copy()

    d = kwargs.get('date')

    if d:
        s, e = d, d
    else:
        s, e = date.period(
            kwargs.get('year'), kwargs.get('month'), kwargs.get('week')
        )

    query['start'] = s.strftime('%Y-%m-%d')
    query['end'] = e.strftime('%Y-%m-%d')

    return query.urlencode()
