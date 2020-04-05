# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.urls import path
from .views import home, journals

app_name = 'main'

urlpatterns = [
    path('journals/', journals.index, name='journals'),
    path('', home.index, name='home'),
]
