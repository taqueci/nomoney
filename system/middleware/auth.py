# Copyright (C) Takeshi Nakamura. All rights reserved.

import re
import urllib

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse

from config.settings import LOGIN_URL, LOGOUT_URL


class AuthMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            return response

        path = request.path
        login = reverse(LOGIN_URL)

        if path != login:
            if path == reverse(LOGOUT_URL):
                url = login
            else:
                next = urllib.parse.quote(request.get_full_path())
                url = '{}?next={}'.format(login, next)

            return HttpResponseRedirect(url)

        return response
