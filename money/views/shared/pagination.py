# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Pagination"""

from django.core.paginator import EmptyPage, PageNotAnInteger


def page(paginator, num):
    """Paginator object"""

    try:
        page_obj = paginator.page(num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj
