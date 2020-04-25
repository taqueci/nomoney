# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.contrib import admin

from config.settings import URL_ROOT
from .models import Account, Journal, Tag, Template

admin.site.site_url = '/{}money/'.format(URL_ROOT)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'entry', 'rank', 'disabled',)


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('date', 'debit', 'credit', 'amount', 'summary', 'disabled',)
    filter_horizontal = ('tags', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'rank', 'disabled')
