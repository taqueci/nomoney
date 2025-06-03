# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Administrator site settings for wine application."""

from django.contrib import admin

from . import models


@admin.register(models.Celler)
class CellerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']


@admin.register(models.Wine)
class WineAdmin(admin.ModelAdmin):
    search_fields = ['display_name', 'region', 'sub_region', 'site']
    list_filter = ['status', 'type', 'colour', 'country']
    list_display = ['lwin', 'display_name', 'country', 'region']


@admin.register(models.Bottle)
class BottleAdmin(admin.ModelAdmin):
    search_fields = ['comment', 'description', 'shop', 'wine__display_name']
    list_display = ['id', 'wine', 'vintage', 'acquired', 'uncorked']
    autocomplete_fields = ['wine']
    filter_horizontal = ['images']
    readonly_fields = ['created', 'updated']
