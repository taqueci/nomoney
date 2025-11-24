# Copyright (C) Takeshi Nakamura. All rights reserved.

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Page


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        if self.instance.content != cleaned_data.get('content'):
            qs = Page.objects.filter(
                digest__isnull=False,
                slug=cleaned_data.get('slug'),
                language=cleaned_data.get('language'),
                content=cleaned_data.get('content'),
            )

            if obj := qs.first():
                raise forms.ValidationError(
                    _('The content is the same as #%(pk)s'),
                    params={'pk': obj.pk},
                )

        return cleaned_data
