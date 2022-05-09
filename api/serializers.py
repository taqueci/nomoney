# Copyright (C) Takeshi Nakamura. All rights reserved.

from rest_framework import serializers

from money.models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'file', 'base_name', 'md5')
