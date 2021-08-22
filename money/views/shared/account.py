# Copyright (C) Takeshi Nakamura. All rights reserved.

from money.models import Account


def grouped_objects():
    return [{
        'entry': x[0],
        'name': x[1],
        'data': Account.objects.filter(entry=x[0]).order_by('-rank')
    } for x in Account.Entry.choices]
