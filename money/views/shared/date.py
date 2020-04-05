# Copyright (C) Takeshi Nakamura. All rights reserved.

import calendar
import datetime
from dateutil.relativedelta import relativedelta


def fy(date=None, month=4, day=1):
    if not date:
        date = datetime.date.today()

    return date.year if date >= date.replace(month=month, day=day) else date.year -1


def range_next_prev(start, end):
    s = datetime.datetime.strptime(start, '%Y-%m-%d')
    e = datetime.datetime.strptime(end, '%Y-%m-%d')

    delta = e - s
    days = delta.days + 1

    if days >= 365:
        n = int(days / 365)

        return {
            'base': {'start': start, 'end': end},
            'next': {
                'start': datetime.date(s.year + n, s.month, s.day),
                'end': datetime.date(e.year + n, e.month, e.day)
            },
            'prev': {
                'start': datetime.date(s.year - n, s.month, s.day),
                'end': datetime.date(e.year - n, e.month, e.day)
            }
        }
    elif days >= 28:
        n = int(days / 28)
        d = relativedelta(months=n)

        return {
            'base': {'start': start, 'end': end},
            'next': {
                'start': _date_for_month(s, s + d),
                'end': _date_for_month(e, e + d)
            },
            'prev': {
                'start': _date_for_month(s, s - d),
                'end': _date_for_month(e, e - d)
            }
        }

    d = relativedelta(weeks=int(days / 7)) if days >= 7 else relativedelta(days=days)

    return {
        'base': {'start': start, 'end': end},
        'next': {'start': s + d, 'end': e + d},
        'prev': {'start': s - d, 'end': e - d}
    }


def _last_day_of_month(dt):
    return calendar.monthrange(dt.year, dt.month)[1]


def _date_for_month(src, dest):
    if src.day == _last_day_of_month(src):
        return dest.replace(day=_last_day_of_month(dest))
    else:
        return dest
