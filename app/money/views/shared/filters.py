# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import forms
from django_filters import rest_framework as filters
from django_filters.rest_framework import MultipleChoiceFilter


class AnyValuesMultipleField(forms.MultipleChoiceField):
    def validate(self, value):
        pass


class AnyValuesMultipleFilter(MultipleChoiceFilter):
    field_class = AnyValuesMultipleField


class KeywordFilter(filters.CharFilter):
    def __init__(self, *args, lookup_expr='icontains', **kwargs):
        super().__init__(*args, lookup_expr=lookup_expr, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs

        for x in value.split():
            qs = qs.filter(**{f'{self.field_name}__{self.lookup_expr}': x})

        return qs
