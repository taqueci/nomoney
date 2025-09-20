# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL configuration for money application."""

from django.urls import path

from .views import charts, home, journals, my, tags, users

app_name = 'money'

urlpatterns = [
    path('journals/', journals.index, name='journals'),
    path('journals/new', journals.new, name='new_journal'),
    path('journals/<pk>', journals.show, name='journal'),
    path('journals/<pk>/edit', journals.edit, name='edit_journal'),
    path('journals/<pk>/destroy', journals.destroy, name='destroy_journal'),

    path('my/account/', my.account, name='my_account'),

    path('reports/', charts.index, name='reports'),
    path('reports/<pk>', charts.show, name='report'),

    path('tags/new', tags.new, name='new_tag'),

    path('users/<name>/', users.show, name='user'),
    path('users/<name>/edit', users.edit, name='edit_user'),

    path('', home.index, name='home'),
]
