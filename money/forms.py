# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import forms
from .models import Journal


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        exclude = (
            'asset', 'liabiity', 'income', 'expense', 'equity',
            'fy', 'year', 'month', 'week',
            'disabled', 'author', 'created', 'updated',
        )
