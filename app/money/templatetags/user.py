# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def user_full_name(user, lang):
    if user.is_anonymous:
        return ''

    return user.full_name(lang)


@register.simple_tag
def user_avatar(user, size=16):
    if url := user.picture_url:
        # pylint: disable-next=line-too-long
        return format_html(
            '<img src="{url}" class="rounded-circle align-text-top" '
            'height="{size}">',
            url=url, size=size,
        )

    return format_html(
        '<span style="font-size: {size}px">'
        '<i class="fas fa-user-circle"></i></span>',
        size=size,
    )
