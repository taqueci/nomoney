# Copyright (C) Takeshi Nakamura. All rights reserved.

import hashlib
import time

from django.db import models
from django.contrib.auth.models import AbstractUser

IMAGE_DIR_USER = 'users'


class User(AbstractUser):
    def file_path(self, filename):
        h = hashlib.md5(f'{self.username}z'.encode()).hexdigest()

        return f'{IMAGE_DIR_USER}/{h}/{int(time.time())}-{filename}'

    image = models.ImageField(null=True, blank=True, upload_to=file_path)

    @property
    def full_name(self):
        name = []

        if self.first_name:
            name.append(self.first_name)

        if self.last_name:
            name.append(self.last_name)

        return ' '.join(name) if name else self.username

    @property
    def full_name_r(self):
        name = []

        if self.last_name:
            name.append(self.last_name)

        if self.first_name:
            name.append(self.first_name)

        return ' '.join(name) if name else self.username

    def __str__(self):
        return self.full_name
