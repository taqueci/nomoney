# Copyright (C) Takeshi Nakamura. All rights reserved.

import os

from django import template

register = template.Library()


@register.filter
def path_basename(value):
    return os.path.basename(value)
