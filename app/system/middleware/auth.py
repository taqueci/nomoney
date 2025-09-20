# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Middleware for authentication."""

import urllib

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse


class AuthMiddleware:  # pylint: disable=too-few-public-methods
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            return self.get_response(request)

        path = request.path
        login = reverse(settings.LOGIN_URL)

        if path == login or not path.startswith(settings.LOGIN_TARGETS):
            return self.get_response(request)

        if path == reverse(settings.LOGOUT_URL):
            url = login
        else:
            next_url = urllib.parse.quote(request.get_full_path())
            url = f'{login}?next={next_url}'

        return HttpResponseRedirect(url)
