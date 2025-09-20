# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Administrator site settings for system."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.User)
class AdminUserAdmin(UserAdmin):
    """The representation of user model."""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
        (_('Setting'), {
            'fields': ('timezone', 'language', 'image'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2',
                'first_name', 'last_name', 'email'
            ),
        }),
    )
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_superuser',
        'last_login',
    )
