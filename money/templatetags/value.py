# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template

register = template.Library()


@register.filter
def value_percent(num, total):
    return 100 * num / total if total > 0 else 0
