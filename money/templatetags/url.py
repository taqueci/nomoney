# Copyright (C) Takeshi Nakamura. All rights reserved.

import os
from django import template

from ..views.shared import date

register = template.Library()


@register.simple_tag(takes_context=True)
def url_param_value(context, key):
    return context['request'].GET.get(key) or ''


@register.simple_tag(takes_context=True)
def url_params(context, **kwargs):
    query = context['request'].GET.copy()

    for key in kwargs.keys():
        query[key] = kwargs[key]

    return query.urlencode()


@register.simple_tag(takes_context=True)
def url_params_sort(context, key):
    query = context['request'].GET.copy()

    sort = context['request'].GET.get('sort')
    order = context['request'].GET.get('order')

    query['sort'] = key

    if (key == sort) and (order == 'asc'):
        query['order'] = 'desc'
    else:
        query['order'] = 'asc'

    return query.urlencode()


@register.simple_tag(takes_context=True)
def url_params_period(context, **kwargs):
    query = context['request'].GET.copy()

    s, e = date.period(kwargs['year'], kwargs.get('month'), kwargs.get('week'))

    query['start'] = s.strftime('%Y-%m-%d')
    query['end'] = e.strftime('%Y-%m-%d')

    return query.urlencode()
