# Copyright (C) Takeshi Nakamura. All rights reserved.

import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def sort_url_params(context, target, key='sort'):
    data = context['request'].GET
    val = data.get(key)

    fields = [target]

    for x in val.split(',') if val else []:
        order, field = re.match(r'(-?)(.*)', x).groups()

        if field == target:
            if order == '-':
                fields.pop(0)
            else:
                fields[0] = f'-{field}'
        else:
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
