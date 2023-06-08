# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Template tags for document page."""

import json

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from ..models import Page

register = template.Library()

PAGE_BADGE_CLASS = {
    Page.Status.DRAFT: 'badge bg-warning',
    Page.Status.DISABLED: 'badge bg-danger',
    Page.Status.BACKUP: 'badge bg-secondary',
}

PAGE_ICON = {
    Page.Status.DRAFT: 'fas fa-fw fa-edit text-warning',
    Page.Status.PUBLISHED: 'fas fa-fw fa-file text-primary',
    Page.Status.DISABLED: 'fas fa-fw fa-ban text-danger',
    Page.Status.BACKUP: 'fas fa-fw fa-copy text-secondary',
}


@register.simple_tag
def page_status_badge(obj):
    """Page status badge."""
    klass = PAGE_BADGE_CLASS.get(obj.status)

    if klass:
        text = obj.get_status_display()
        return mark_safe(f'<span class="{klass}">{text}</span>')

    return ''


@register.filter
def page_tree_data(obj, queryset):
    """Data for jsTree."""
    slug = _page_slug(obj)
    pages = queryset

    data = []

    for p in pages:
        href = reverse('doc:page', kwargs={'slug': p.slug})
        p_slug = _page_slug(p)
        text = p.title

        if p.status != Page.Status.PUBLISHED:
            updated = p.updated.strftime('%Y-%m-%d %H:%M:%S')
            text += f' (#{p.pk} {updated})'
            href += f'?id={p.pk}'

        data.append({
            'id': f'page-{p_slug}',
            'text': text,
            'icon': PAGE_ICON.get(p.status),
            'parent': f'page-{p.parent.slug}' if p.parent else '#',
            'state': {'selected': p_slug == slug},
            'a_attr': {'href': href},
        })

    return json.dumps(data)


@register.filter
def page_breadcrumb_items(obj, queryset):
    """Breadcrumb items."""
    items = [obj]
    index = {x.pk: x for x in queryset}

    p = obj

    while p.parent:
        items.append(index[p.parent.pk])
        p = index[p.parent.pk]

    return reversed(items)


def _page_slug(obj):
    if not obj:
        return None

    published = obj.status == Page.Status.PUBLISHED

    return obj.slug if published else f'{obj.slug}--{obj.pk}'
