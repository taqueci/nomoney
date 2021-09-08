# Copyright (C) Takeshi Nakamura. All rights reserved.

import urllib

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse

from config.settings import LOGIN_URL, LOGOUT_URL, LOGIN_TARGETS


# pylint: disable=too-few-public-methods
class AuthMiddleware(MiddlewareMixin):
    # pylint: disable=no-self-use
    def process_response(self, request, response):
        if request.user.is_authenticated:
            return response

        path = request.path
        login = reverse(LOGIN_URL)

        if path == login or not path.startswith(LOGIN_TARGETS):
            return response

        if path == reverse(LOGOUT_URL):
            url = login
        else:
            next_url = urllib.parse.quote(request.get_full_path())
            url = f'{login}?next={next_url}'

        return HttpResponseRedirect(url)
