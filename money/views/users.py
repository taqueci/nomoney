# Copyright (C) Takeshi Nakamura. All rights reserved.

import zoneinfo

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from ..forms import UserForm

UserModel = get_user_model()


def show(request: HttpRequest, name: str) -> HttpResponse:
    obj = get_object_or_404(UserModel, username=name)

    return render(request, 'money/users/show.html', {
        'object': obj
    })


def edit(request: HttpRequest, name: str) -> HttpResponse:
    obj = get_object_or_404(UserModel, username=name)

    if not _is_allowed(request.user, obj):
        raise PermissionDenied  # 403

    if request.method == 'POST':
        return update(request, obj)

    return render(request, 'money/users/edit.html', {
        'object': obj, 'timezones': sorted(zoneinfo.available_timezones()),
    })


def update(request: HttpRequest, obj) -> HttpResponseRedirect:
    form = UserForm(request.POST, request.FILES, instance=obj)

    if form.is_valid():
        new_obj = form.save(commit=False)

        if request.POST.get('image_clear'):
            new_obj.image = None

        new_obj.save()

        messages.success(request, _('The item has been successfully updated'))
    else:
        messages.error(request, _('Failed to update the item'))

    to = request.GET.get('next')

    return redirect(to) if to else redirect('money:user', name=obj.username)


def _is_allowed(user, obj) -> bool:
    return (user == obj) or user.is_superuser
