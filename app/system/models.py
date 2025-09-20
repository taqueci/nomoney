# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Models for system."""

import hashlib
import time

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from user_g11n.models import UserLanguageSupportMixin, UserTimeZoneSupportMixin

IMAGE_DIR_USER = 'users'
TIME_ZONE = settings.TIME_ZONE


class User(UserLanguageSupportMixin, UserTimeZoneSupportMixin, AbstractUser):
    """Custom user class."""

    # Override default time zone
    UserTimeZoneSupportMixin._meta.get_field('timezone').default = TIME_ZONE

    def file_path(self, filename):
        """File path for user image."""

        md5 = hashlib.md5(f'{self.username}z'.encode()).hexdigest()

        return f'{IMAGE_DIR_USER}/{md5}/{int(time.time())}-{filename}'

    image = models.ImageField(null=True, blank=True, upload_to=file_path)

    def full_name(self, language=None):
        """Return full name."""

        names = [x for x in (self.first_name, self.last_name) if x]

        if _is_last_name_first(language):
            names.reverse()

        return ' '.join(names) if names else self.username

    def __str__(self):
        return self.full_name()


def _is_last_name_first(lang):
    return lang in ('hu', 'ja', 'ko', 'vi', 'zh-hans', 'zh-hant')
