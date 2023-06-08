# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Views for documents."""

from functools import reduce

from bs4 import BeautifulSoup
from django.contrib.postgres.search import (
    SearchHeadline, SearchQuery, SearchRank, SearchVector,
)
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils.translation import get_language

from config.settings import MEDIA_URL
from money.models import Attachment

from .models import Page

IMAGE_TYPES = ('.jpeg', '.jpg', '.png')

HTML_CONTENT_CLASS = 'doc-content'


def admin_images(request):
    """Image source list for administrator page."""
    if not request.user.is_superuser:
        raise PermissionDenied

    objs = Attachment.objects.filter(
        reduce(lambda x, y: x | y, [Q(file__endswith=t) for t in IMAGE_TYPES])
    ).order_by('-created')

    return JsonResponse([{
        'title': x.base_name, 'value': x.file.url,
    } for x in objs], safe=False)


def admin_links(request):
    """Attachment link list for administrator page."""
    if not request.user.is_superuser:
        raise PermissionDenied

    objs = Attachment.objects.all().order_by('-created')

    return JsonResponse([{
        'title': x.base_name, 'value': x.file.url,
    } for x in objs], safe=False)


def render_page(request, template_name, context=None):
    """Returns an HttpResponse with appending timestamp to media file paths."""
    content = loader.render_to_string(template_name, context, request)
    soup = BeautifulSoup(content, 'html.parser')

    latest_attachment = Attachment.objects.all().order_by('-created').first()
    timestamp = int(latest_attachment.created.timestamp())

    for x in soup.find(class_=HTML_CONTENT_CLASS).find_all('a'):
        if x.get('href', '').startswith(MEDIA_URL):
            x['href'] += f'?v={timestamp}'

    for x in soup.find(class_=HTML_CONTENT_CLASS).find_all('img'):
        if x['src'].startswith(MEDIA_URL):
            x['src'] += f'?v={timestamp}'

    return HttpResponse(str(soup))


def pages(request):
    """Document index view."""
    if request.GET.get('q'):
        return search(request)

    lang = request.GET.get('lang', get_language())
    objs = _page_objects(request.user, lang, request.GET.get('all'))
    context = {'objs': _reduced_pages(objs)}

    return render(request, 'doc/pages/index.html', context)


def page(request, slug):
    """Document page view."""
    lang = request.GET.get('lang', get_language())
    pk = request.GET.get('id')

    if pk:
        objs = _page_objects(request.user, lang, True)
        obj = objs.filter(slug=slug, pk=pk).first()
    else:
        objs = _page_objects(request.user, lang)
        obj = objs.filter(slug=slug).first()

    if not obj:
        raise Http404

    if request.GET.get('export') == 'html':
        context = {'obj': obj, 'action': request.GET.get('action')}
        return render(request, 'doc/pages/page.html', context)

    context = {'obj': obj, 'objs': _reduced_pages(objs)}
    return render_page(request, 'doc/pages/show.html', context)


def search(request):
    """Document search view."""
    vector = SearchVector('title', 'content')
    query = SearchQuery(request.GET['q'])

    objs = Page.objects.annotate(
        rank=SearchRank(vector, query),
        headline=SearchHeadline(
            'content',
            query,
            start_sel='<mark><span class="text-danger">',
            stop_sel='</span></mark>',
        ),
    ).filter(
        rank__gt=0,
        status=Page.Status.PUBLISHED,
    ).order_by('-rank')

    return render(request, 'doc/pages/search.html', {'objs': objs})


def _page_objects(user, lang, all_pages=False):
    arg = {'language__in': ('', lang)}

    if not all_pages:
        arg['status'] = Page.Status.PUBLISHED

    return Page.objects.accessible(user).filter(**arg).order_by(
        'parent', 'order', 'slug', '-language', '-status', '-updated',
    )


def _reduced_pages(qs):
    """Drop duplicated published pages."""
    objs = []
    slugs = []

    for x in qs:
        published = x.status == Page.Status.PUBLISHED

        # Use the first published page only.
        if published and (x.slug in slugs):
            continue

        objs.append(x)

        if published:
            slugs.append(x.slug)

    return objs
