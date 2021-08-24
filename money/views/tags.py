# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.http import Http404
from django.http.response import JsonResponse

from money.models import Tag


def new(request):
    if request.method != 'POST':
        raise Http404()

    name = request.POST.get('name')

    obj = Tag(name=name)
    obj.save()

    return JsonResponse({'id': obj.pk, 'name': name})
