# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Forms for system."""

from django.contrib.auth.forms import PasswordChangeForm


class UserPasswordChangeForm(PasswordChangeForm):
    """Helper class for the form of changing password."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # For Bootstrap 4
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
