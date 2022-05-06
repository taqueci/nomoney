# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def sort_url_params(context, target, key='sort'):
    data = context['request'].GET
    val = data.get(key)
    vals = val.split(',') if val else []

    target_asc = target
    target_desc = f'-{target}'

    fields = []

    if len(vals) > 0 and vals[0] == target_asc:
        fields.append(target_desc)
    elif len(vals) > 0 and vals[0] == target_desc:
        pass
    elif target_desc in vals:
        fields.append(target_desc)
    else:
        fields.append(target_asc)

    for x in vals:
        if x not in (target_asc, target_desc):
            fields.append(x)

    query = data.copy()
    query[key] = ','.join(fields)

    return query.urlencode()


@register.simple_tag(takes_context=True)
def sort_icon(context, target, key='sort'):
    data = context['request'].GET
    val = data.get(key)

    for x in val.split(',') if val else []:
        if x == target:
            return mark_safe('<i class="fas fa-sort-up text-muted"></i>')

        if x == f'-{target}':
            return mark_safe('<i class="fas fa-sort-down text-muted"></i>')

    return ''
