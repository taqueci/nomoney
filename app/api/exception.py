# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None and isinstance(exc, IntegrityError):
        data = {
            'detail': str(exc),
        }

        return Response(data, status=status.HTTP_409_CONFLICT)

    return response
