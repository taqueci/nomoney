# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Models for system."""

import hashlib
import os
import struct
import time

from django.contrib.auth.models import AbstractUser
from django.db import models
from user_g11n.models import UserLanguageSupportMixin, UserTimeZoneSupportMixin

IMAGE_DIR_USER = 'users'


class Digest64Field(models.BigIntegerField):
    # pylint: disable=unused-argument
    def from_db_value(self, value, expression, connection):
        return self._to_unsigned(value)

    def to_python(self, value):
        if isinstance(value, str):
            return int(value)

        return value

    def get_prep_value(self, value):
        if value is None:
            return None

        return self._to_signed(int(value))

    def _to_unsigned(self, signed_value):
        if signed_value is None:
            return None

        return struct.unpack('Q', struct.pack('q', signed_value))[0]

    def _to_signed(self, unsigned_value):
        if unsigned_value is None:
            return None

        return struct.unpack('q', struct.pack('Q', unsigned_value))[0]


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

        d = format(self.digest, '016x')

        return os.path.join(self.FILE_PATH_PREFIX, d[:2], d, filename)

    file = models.FileField(upload_to=upload_to)
    digest = Digest64Field(default=0)

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        if not self.digest:
            self.digest = self.get_digest()

        super().save(*args, **kwargs)

    def get_digest(self):
        md5 = hashlib.md5()

        for chunk in self.file.chunks():
            md5.update(chunk)

        return int.from_bytes(md5.digest()[:8])

    @property
    def base_name(self) -> str:
        return os.path.basename(self.file.name)


def _is_last_name_first(lang):
    return lang in ('hu', 'ja', 'ko', 'vi', 'zh-hans', 'zh-hant')
