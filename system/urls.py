# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

app_name = 'system'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='system/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
