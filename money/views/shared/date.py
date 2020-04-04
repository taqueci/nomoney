# Copyright (C) Takeshi Nakamura. All rights reserved.

import datetime


def fy(date=None, month=4, day=1):
    if not date:
        date = datetime.date.today()

    return date.year if date >= date.replace(month=month, day=day) else date.year -1
