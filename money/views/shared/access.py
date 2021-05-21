# Copyright (C) Takeshi Nakamura. All rights reserved.


def creatable(user):
    return user.is_staff


def readable(user):
    return True


def updatable(user):
    return user.is_staff


def deletable(user):
    return user.is_staff
