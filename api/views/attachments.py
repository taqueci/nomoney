# Copyright (C) Takeshi Nakamura. All rights reserved.

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import AttachmentSerializer


class List(APIView):
    parser_classes = (MultiPartParser, )

    # pylint: disable-next=redefined-builtin,unused-argument
    def post(self, request, format=None):
        serializer = AttachmentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
