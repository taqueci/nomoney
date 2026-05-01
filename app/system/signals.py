# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Signals for system."""

import logging
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.core.mail import mail_admins
from django.dispatch import receiver
from django.utils import timezone

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
# pylint: disable-next=unused-argument
def notify_admin_on_login(sender, request, user, **kwargs):
    if not settings.EMAIL_HOST or user.is_verified:
        return

    last_login = timezone.localtime(user.last_login)

    message = '\n'.join([
        'Non-verified user login:',
        f'- User: {user.username}',
        f'- Time: {last_login}',
    ])

    try:
        mail_admins('Non-verified user login', message)
    # pylint: disable-next=broad-exception-caught
    except (SMTPException, Exception) as e:
        logger.error(e, exc_info=True)
