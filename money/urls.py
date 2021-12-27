# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL configuration for money application."""

from django.urls import path

from .views import home, journals, reports, tags

app_name = 'money'

urlpatterns = [
    path('journals/', journals.index, name='journals'),
    path('journals/new', journals.new, name='new_journal'),
    path('journals/<pk>', journals.show, name='journal'),
    path('journals/<pk>/edit', journals.edit, name='edit_journal'),
    path('journals/<pk>/destroy', journals.destroy, name='destroy_journal'),

    path('reports/', reports.index, name='reports'),
    path('reports/<pk>', reports.show, name='report'),

    path('tags/new', tags.new, name='new_tag'),

    path('', home.index, name='home'),
]
