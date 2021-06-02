# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Forms for money application."""

from django import forms
from .models import Journal


class JournalForm(forms.ModelForm):
    """Helper class for the form of journal model."""

    class Meta:
        model = Journal
        fields = (
            'debit', 'credit', 'date', 'amount', 'summary', 'note', 'tags',
        )
