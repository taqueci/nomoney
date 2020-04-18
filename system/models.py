# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        name = []

        if self.first_name:
            name.append(self.first_name)

        if self.last_name:
            name.append(self.last_name)

        return ' '.join(name) if name else self.username
