# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.shortcuts import render


def index(request):
    return render(request, 'money/home/index.html', {})
