# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import forms
from django_filters.rest_framework import MultipleChoiceFilter


class AnyValuesMultipleField(forms.MultipleChoiceField):
    def validate(self, value):
        pass


class AnyValuesMultipleFilter(MultipleChoiceFilter):
    field_class = AnyValuesMultipleField
