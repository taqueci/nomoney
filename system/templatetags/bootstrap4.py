# Copyright (C) Takeshi Nakamura. All rights reserved.

"""
BSD 3-Clause License

Copyright (c) Zostera B.V. and individual contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# To prevent trouble caused by local install of django-bootstrap4

from django import template
from django.contrib.messages import constants as message_constants

register = template.Library()

MESSAGE_LEVEL_CLASSES = {
    message_constants.DEBUG: 'alert alert-warning',
    message_constants.INFO: 'alert alert-info',
    message_constants.SUCCESS: 'alert alert-success',
    message_constants.WARNING: 'alert alert-warning',
    message_constants.ERROR: 'alert alert-danger',
}


@register.filter
def bootstrap_message_classes(message):
    extra_tags = None

    try:
        extra_tags = message.extra_tags
    except AttributeError:
        pass

    if not extra_tags:
        extra_tags = ''

    classes = [extra_tags]

    try:
        level = message.level
    except AttributeError:
        pass
    else:
        try:
            classes.append(MESSAGE_LEVEL_CLASSES[level])
        except KeyError:
            classes.append('alert alert-danger')

    return ' '.join(classes).strip()
