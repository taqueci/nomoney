# Copyright (C) Takeshi Nakamura. All rights reserved.

from rest_framework import serializers

from money import models


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Journal
        fields = ('debit', 'credit')
