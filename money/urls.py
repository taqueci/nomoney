# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.urls import path
from .views import home

app_name = 'main'

urlpatterns = [
    path('', home.index, name='home'),
]
