# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Models for system."""

import hashlib
import time

from django.db import models
from django.contrib.auth.models import AbstractUser

IMAGE_DIR_USER = 'users'


class User(AbstractUser):
    """Custom user class."""

    def file_path(self, filename):
        """File path for user image."""

        md5 = hashlib.md5(f'{self.username}z'.encode()).hexdigest()

        return f'{IMAGE_DIR_USER}/{md5}/{int(time.time())}-{filename}'

    image = models.ImageField(null=True, blank=True, upload_to=file_path)

    @property
    def full_name(self):
        """Return full name."""

        name = []

        if self.first_name:
            name.append(self.first_name)

        if self.last_name:
            name.append(self.last_name)

        return ' '.join(name) if name else self.username

    @property
    def full_name_r(self):
        """Return reversed full name."""

        name = []

        if self.last_name:
            name.append(self.last_name)

        if self.first_name:
            name.append(self.first_name)

        return ' '.join(name) if name else self.username

    def __str__(self):
        return self.full_name
