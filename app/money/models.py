# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Models for money application."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from system.models import Attachment

from .views.shared import date

UserModel = get_user_model()


class BaseQuerySet(models.QuerySet):
    """Base query set."""

    def available(self):
        """Filter for getting available objects."""

        return self.filter(enabled=True)


class Account(models.Model):
    """Account model."""

    # pylint: disable-next=too-many-ancestors
    class Entry(models.IntegerChoices):
        """Choices for an account etnry."""

        ASSET = 1, _('Asset')
        LIABILITY = 2, _('Liability')
        INCOME = 3, _('Income')
        EXPENSE = 4, _('Expense')
        EQUITY = 5, _('Equity')

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    entry = models.IntegerField(choices=Entry.choices)

    rank = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True)

    objects = BaseQuerySet.as_manager()

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag model."""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# pylint: disable=R0902
class Journal(models.Model):
    """Journal model."""

    debit = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='journal_debit'
    )
    credit = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='journal_credit'
    )

    date = models.DateField()
    amount = models.IntegerField()
    summary = models.CharField(max_length=255)
    note = models.TextField(null=True, blank=True)

    tags = models.ManyToManyField(Tag, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)

    asset = models.IntegerField(blank=True, default=0, editable=False)
    liability = models.IntegerField(blank=True, default=0, editable=False)
    income = models.IntegerField(blank=True, default=0, editable=False)
    expense = models.IntegerField(blank=True, default=0, editable=False)
    equity = models.IntegerField(blank=True, default=0, editable=False)

    # pylint: disable=C0103
    fy = models.IntegerField(
        blank=True, default=0, editable=False, verbose_name=_('Financial year')
    )

    enabled = models.BooleanField(default=True)

    author = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BaseQuerySet.as_manager()

    def __str__(self):
        return f'#{self.pk}'

    def _entry_amount(self, entry):
        a_d = self.amount if self.debit.entry == entry else 0
        a_c = self.amount if self.credit.entry == entry else 0

        return a_d - a_c

    def save(self, *args, **kwargs):
        self.asset = self._entry_amount(Account.Entry.ASSET)
        self.liability = -self._entry_amount(Account.Entry.LIABILITY)
        self.income = -self._entry_amount(Account.Entry.INCOME)
        self.expense = self._entry_amount(Account.Entry.EXPENSE)
        self.equity = -self._entry_amount(Account.Entry.EQUITY)

        self.fy = date.fy(
            self.date, settings.FY_START_MONTH, settings.FY_START_DAY
        )

        super().save(*args, **kwargs)


class Template(models.Model):
    """Template model."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    debit = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='template_debit'
    )
    credit = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='template_credit'
    )

    date = models.CharField(max_length=255, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    summary = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    rank = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True)

    objects = BaseQuerySet.as_manager()

    def __str__(self):
        return self.name
