# Copyright (C) Takeshi Nakamura. All rights reserved.

import unicodedata


def normalize_string_fields(obj, *fields):
    """Normalize string fields of the model."""

    for x in fields:
        if not hasattr(obj, x):
            continue

        val = unicodedata.normalize('NFKC', getattr(obj, x).strip())
        setattr(obj, x, val)
