# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Administrator site settings for document application."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


class PageActiveListFilter(admin.SimpleListFilter):
    """List filter for getting active pages."""
    title = _('active')
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return ((1, _('Yes')), (0, _('No')))

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        actives = (models.Page.Status.DRAFT, models.Page.Status.PUBLISHED)

        if self.value() == '1':
            return queryset.filter(status__in=actives)

        return queryset.exclude(status__in=actives)


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    """The representation of page model."""
    search_fields = ('title', 'slug', 'note')
    list_display = (
        'id', 'title', 'slug', 'language', 'status', 'order', 'updated',
    )
    list_filter = (PageActiveListFilter, 'status', 'slug', 'language')
    readonly_fields = ['author', 'created', 'updated']
    change_form_template = 'doc/admin/change_form.html'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)
