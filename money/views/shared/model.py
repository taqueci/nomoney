# Copyright (C) Takeshi Nakamura. All rights reserved.

import unicodedata


def normalize_string_fields(obj, *fields):
    """Normalize string fields of the model."""

    for x in fields:
        s = getattr(obj, x) if hasattr(obj, x) else None

        if s is None:
            continue

        setattr(obj, x, unicodedata.normalize('NFKC', s.strip()))
