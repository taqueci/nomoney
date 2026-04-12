# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def asset_load_css(path):
    asset = settings.ASSETS_LIST[path]
    attrs = {'rel': 'stylesheet'}

    if settings.ASSETS_CDN and asset.get('cdn'):
        attrs.update(**asset['cdn'])
    else:
        attrs['href'] = static(path)

    html_attr = ' '.join([f'{k}="{v}"' for k, v in attrs.items()])

    return mark_safe(f'<link {html_attr}>')


@register.simple_tag
def asset_load_js(path):
    asset = settings.ASSETS_LIST[path]
    attrs = {}

    if settings.ASSETS_CDN and asset.get('cdn'):
        attrs.update(**asset['cdn'])
    else:
        attrs['src'] = static(path)

    html_attr = ' '.join([f'{k}="{v}"' for k, v in attrs.items()])

    return mark_safe(f'<script {html_attr}></script>')
