# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template

from ..views.shared import date

register = template.Library()


@register.simple_tag(takes_context=True)
def url_param_value(context, key):
    return context['request'].GET.get(key, '')


@register.simple_tag(takes_context=True)
def url_params_period(context, date_obj):
    query = context['request'].GET.copy()
    unit = query.get('unit', 'year')

    if unit == 'year':
        s, e = date.period(date_obj.year, None, None)
    elif unit == 'month':
        s, e = date.period(date_obj.year, date_obj.month, None)
    elif unit == 'week':
        s, e = date.period(date_obj.year, None, date_obj.isocalendar()[1])
    else:
        s, e = date_obj, date_obj

    query['start'] = s.strftime('%Y-%m-%d')
    query['end'] = e.strftime('%Y-%m-%d')

    return query.urlencode()
