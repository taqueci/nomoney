# Copyright (C) Takeshi Nakamura. All rights reserved.

from money.models import Account

UNDEFINED = 0
INCOMING = 1
OUTGOING = 2
REPAYMENT = 3


def category(obj):
    if obj.credit.entry == Account.Entry.INCOME:
        return INCOMING
    if obj.debit.entry == Account.Entry.EXPENSE:
        return OUTGOING
    if obj.debit.entry == Account.Entry.LIABILITY:
        return REPAYMENT

    return UNDEFINED
