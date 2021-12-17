# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Views for system."""

from django.contrib.auth.views import (
    PasswordChangeDoneView, PasswordChangeView,
)
from django.urls import reverse_lazy

from .forms import UserPasswordChangeForm


class PasswordChange(PasswordChangeView):
    """View for changing password."""

    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('system:password_change_done')
    template_name = 'system/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """View after changing password."""

    template_name = 'system/password_change_done.html'
