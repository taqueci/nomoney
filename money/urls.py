# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.urls import path
from .views import home, journals

app_name = 'main'

urlpatterns = [
    path('journals/', journals.index, name='journals'),
    path('journals/new', journals.new, name='new_journal'),
    path('journals/<id>', journals.show, name='journal'),
    path('journals/<id>/edit', journals.edit, name='edit_journal'),
    path('journals/<id>/destroy', journals.destroy, name='destroy_journal'),

    path('', home.index, name='home'),
]
