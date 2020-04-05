# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template

register = template.Library()


@register.simple_tag
def html_selected_if_eq(a, b):
    return 'selected' if a == b else ''


@register.simple_tag(takes_context=True)
def html_selected_by_query_list(context, key, value):
    vals = list(context['request'].GET.getlist(key))

    return 'selected' if str(value) in vals else ''
