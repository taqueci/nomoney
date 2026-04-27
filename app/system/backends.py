# Copyright (C) Takeshi Nakamura. All rights reserved.

"""Backends."""

from social_core.backends import google


class GoogleOAuth2(google.GoogleOAuth2):
    def get_user_details(self, response):
        detail = super().get_user_details(response)
        detail['image_url'] = response.get('picture')

        return detail
