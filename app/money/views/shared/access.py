# Copyright (C) Takeshi Nakamura. All rights reserved.


def creatable(user):
    return user.has_perm('money.add_journal')


def readable(user):
    return not user.is_anonymous


def updatable(user):
    return user.has_perm('money.change_journal')


def deletable(user):
    return user.has_perm('money.delete_journal')
