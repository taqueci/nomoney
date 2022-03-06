# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import template

from ..views.shared import access

register = template.Library()


@register.filter
def access_creatable(user):
    return access.creatable(user)


@register.filter
def access_updatable(user):
    return access.updatable(user)


@register.filter
def access_deletable(user):
    return access.deletable(user)
