# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView
)

from django.urls import reverse_lazy

from .forms import UserPasswordChangeForm


class PasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('system:password_change_done')
    template_name = 'system/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'system/password_change_done.html'
