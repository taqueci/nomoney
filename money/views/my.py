# Copyright (C) Takeshi Nakamura. All rights reserved.

from . import users


def account(request):
    return users.show(request, request.user.username)
