# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Serializer for APIs."""

from rest_framework import serializers

from money import models


class JournalSerializer(serializers.ModelSerializer):
    """Serializer class for journal model."""

    class Meta:
        model = models.Journal
        fields = ('debit', 'credit')
