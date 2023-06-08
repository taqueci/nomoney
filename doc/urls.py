# Copyright (C) Takeshi Nakamura. All rights reserved.

"""URL configuration for document application."""

from django.urls import include, path

from . import views

app_name = 'doc'

urlpatterns = [
    path('__admin__/images', views.admin_images, name='admin_images'),
    path('__admin__/links', views.admin_links, name='admin_links'),
    path('__tinymce__/', include('tinymce.urls')),
    path('<slug>', views.page, name='page'),
    path('', views.pages, name='pages'),
]
