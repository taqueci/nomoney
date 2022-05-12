# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Administrator site settings for money application."""

from django.contrib import admin

from config.settings import SITE_URL

from .models import Account, Attachment, Journal, Tag, Template

admin.site.site_url = SITE_URL


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """The representation of account model."""

    list_display = ('name', 'description', 'entry', 'rank', 'enabled',)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """The representation of attachment model."""

    list_display = ('id', 'file', 'author', 'created')


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    """The representation of journal model."""

    list_display = (
        'date', 'debit', 'credit', 'amount', 'summary', 'enabled',
    )
    filter_horizontal = ('tags', 'attachments')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """The representation of tag model."""

    list_display = ('name', )


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """The representation of template model."""

    list_display = ('name', 'description', 'rank', 'enabled')
