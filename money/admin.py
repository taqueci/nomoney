# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.contrib import admin
from .models import Account, Journal


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'entry', 'rank', 'disabled',)


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('date', 'debit', 'credit', 'amount', 'summary', 'disabled',)
