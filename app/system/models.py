# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Models for system."""

import hashlib
import os
import time

from django.contrib.auth.models import AbstractUser
from django.db import models
from user_g11n.models import UserLanguageSupportMixin, UserTimeZoneSupportMixin

IMAGE_DIR_USER = 'users'


class User(UserLanguageSupportMixin, UserTimeZoneSupportMixin, AbstractUser):
    """Custom user class."""

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


class Attachment(models.Model):
    """Attachment model."""

    FILE_PATH_PREFIX = 'attachments'

    def upload_to(self, filename: str) -> str:
        """ File path for attachment."""

        md5 = self.md5

        return os.path.join(self.FILE_PATH_PREFIX, md5[:2], md5, filename)

    file = models.FileField(upload_to=upload_to)
    md5 = models.CharField(max_length=36, editable=False)

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        md5 = hashlib.md5()

        for chunk in self.file.chunks():
            md5.update(chunk)

        self.md5 = md5.hexdigest()

        super().save(*args, **kwargs)

    @property
    def base_name(self) -> str:
        return os.path.basename(self.file.name)


def _is_last_name_first(lang):
    return lang in ('hu', 'ja', 'ko', 'vi', 'zh-hans', 'zh-hant')
