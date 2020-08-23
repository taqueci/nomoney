# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.contrib.auth.forms import PasswordChangeForm


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # For Bootstrap 4
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
