# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Forms for money application."""

from django import forms
from django.contrib.auth import get_user_model

from .models import Journal

UserModel = get_user_model()


class JournalForm(forms.ModelForm):
    """Helper class for the form of journal model."""

    class Meta:
        model = Journal
        fields = (
            'debit', 'credit', 'date', 'amount', 'summary', 'note', 'tags',
            'attachments',
        )


class UserForm(forms.ModelForm):
    """Helper class for the form of user model."""

    class Meta:
        model = UserModel
        fields = ('image', 'timezone', 'language')
