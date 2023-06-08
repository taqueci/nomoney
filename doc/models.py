# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Models for document application."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce import models as tinymce_models

User = get_user_model()


class PageQuerySet(models.QuerySet):
    """Query set for Page model."""
    def accessible(self, user):
        """Returns a query set that is accessible by the user.

        Args:
            user (User): A user object.

        Returns:
            QuerySet: A query set.
        """
        return self if user.is_superuser else self.filter(
            status=Page.Status.PUBLISHED,
        )


class Page(models.Model):
    """"Document page model."""
    class Status(models.IntegerChoices):
        """Status choices."""
        DRAFT = 0, _('Draft')
        PUBLISHED = 100, _('Published')
        DISABLED = -100, _('Disabled')
        BACKUP = -200, _('Backup')

    title = models.CharField(max_length=255)
    content = tinymce_models.HTMLField(blank=True)

    language = models.CharField(
        max_length=7, blank=True,
        choices=settings.LANGUAGES, default='en',
    )

    slug = models.SlugField()
    order = models.IntegerField(default=100)

    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT)
    note = models.TextField(blank=True)

    parent = models.ForeignKey(
        'Page', null=True, blank=True, on_delete=models.PROTECT
    )

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PageQuerySet.as_manager()

    def __str__(self):
        return f'#{self.pk} {self.title}'

    def save(self, *args, **kwargs):
        if self.pk:
            self._pre_save()
        super().save(*args, **kwargs)

    def is_accessible(self, user):
        """Wheather an object is accessible or not."""
        return Page.objects.filter(pk=self.pk).accessible(user).exists()

    def _pre_save(self):
        """Creates backup of page."""
        obj = Page.objects.get(pk=self.pk)
        updated = obj.updated

        if obj.status != self.Status.PUBLISHED:
            return

        if self.status == self.Status.PUBLISHED:
            status = self.Status.BACKUP
        elif self.status == self.Status.DRAFT:
            status = self.Status.PUBLISHED
        else:
            return

        # Clone instance.
        obj.pk = None
        obj.status = status
        obj.save()

        # Restore field 'updated' by force.
        Page.objects.filter(pk=obj.pk).update(updated=updated)
