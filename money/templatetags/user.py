# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def user_full_name(user, lang):
    if user.is_anonymous:
        return ''

    return user.full_name if lang != 'ja' else user.full_name_r


@register.simple_tag
def user_avatar(user, size=16):
    if hasattr(user, 'image') and user.image:
        # pylint: disable=line-too-long
        return mark_safe(f'<img src="{user.image.url}" class="rounded-circle align-text-top" height="{size}">')

    return mark_safe(f'<span style="font-size: {size}px"><i class="fas fa-user-circle"></i></span>')
