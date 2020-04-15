# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from config import settings
from .views.shared import date

UserModel = get_user_model()


class Account(models.Model):
    ENTRY_ASSET = 1
    ENTRY_LIABILITY = 2
    ENTRY_INCOME = 3
    ENTRY_EXPENSE = 4
    ENTRY_EQUITY = 5

    ENTRY_CHOICES = (
        (ENTRY_ASSET, _('Asset')),
        (ENTRY_LIABILITY, _('Liability')),
        (ENTRY_INCOME, _('Income')),
        (ENTRY_EXPENSE, _('Expense')),
        (ENTRY_EQUITY, _('Equity')),
    )

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    entry = models.IntegerField(choices=ENTRY_CHOICES)

    rank = models.IntegerField(default=0)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Journal(models.Model):
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

    tags  = models.ManyToManyField(Tag, blank=True)

    asset = models.IntegerField(blank=True, default=0)
    liability = models.IntegerField(blank=True, default=0)
    income = models.IntegerField(blank=True, default=0)
    expense = models.IntegerField(blank=True, default=0)
    equity = models.IntegerField(blank=True, default=0)

    fy = models.IntegerField(
        blank=True, default=0, verbose_name=_('Financial year')
    )
    year = models.IntegerField(blank=True, default=0)
    month = models.IntegerField(blank=True, default=0)
    week = models.IntegerField(blank=True, default=0)

    disabled = models.BooleanField(default=False)

    author = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def _entry_amount(self, entry):
        d = self.amount if self.debit.entry == entry else 0
        c = self.amount if self.credit.entry == entry else 0

        return d - c

    def save(self, *args, **kwargs):
        self.asset = self._entry_amount(Account.ENTRY_ASSET)
        self.liability = -self._entry_amount(Account.ENTRY_LIABILITY)
        self.income = -self._entry_amount(Account.ENTRY_INCOME)
        self.expense = self._entry_amount(Account.ENTRY_EXPENSE)
        self.equity = -self._entry_amount(Account.ENTRY_EQUITY)

        self.fy = date.fy(self.date, settings.FY_START_MONTH, settings.FY_START_DAY)
        self.year = self.date.year
        self.month = self.date.month
        self.week = self.date.isocalendar()[1]

        super(Journal, self).save(*args, **kwargs)


class Template(models.Model):
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

    rank = models.IntegerField(default=0)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
