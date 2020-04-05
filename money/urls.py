# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.urls import path
from .views import home, journals

app_name = 'main'

urlpatterns = [
    path('journals/', journals.index, name='journals'),
    path('journals/new', journals.new, name='new_journal'),
    path('journals/<id>', journals.show, name='journal'),
    path('', home.index, name='home'),
]
