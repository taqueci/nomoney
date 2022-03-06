# Copyright (C) Takeshi Nakamura. All rights reserved.

"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from os import environ as env
from pathlib import Path

from . import version

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f28)f6n)+po@miei(tn**ki05n@@5z-caf8y!hrz#&-n8p09i@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = env.get('N_ALLOWED_HOSTS', 'localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_filters',
    'rest_framework',
    'system',
    'money',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'system.middleware.auth.AuthMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'config.context_processors.site_values',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.get('N_DATABASE_ENGINE'),
        'HOST': env.get('N_DATABASE_HOST'),
        'PORT': env.get('N_DATABASE_PORT'),
        'NAME': env.get('N_DATABASE_NAME'),
        'USER': env.get('N_DATABASE_USER'),
        'PASSWORD': env.get('N_DATABASE_PASSWORD'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = env.get('N_LANGUAGE_CODE', 'en-us')

TIME_ZONE = env.get('N_TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

URL_PREFIX = env.get('N_URL_PREFIX', '/n')

ROUTE_PREFIX = URL_PREFIX[1:]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = env.get('N_STATIC_URL', f'{URL_PREFIX}/static/')

STATIC_ROOT = env.get('N_STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles'))

MEDIA_URL = env.get('N_MEDIA_URL', f'{URL_PREFIX}/media/')

MEDIA_ROOT = env.get('N_MEDIA_ROOT',  os.path.join(BASE_DIR, 'media'))

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'system.User'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'money', 'locale'),
)

LOGIN_URL = 'system:login'
LOGIN_REDIRECT_URL = 'money:home'
LOGOUT_URL = 'system:logout'
LOGOUT_REDIRECT_URL = 'system:login'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Number of digits for filter initcomma
NUMBER_GROUPING = 3

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

FY_START_MONTH = 4
FY_START_DAY = 1

NAME = env.get('N_NAME', 'NoMoney')

VERSION = version.VERSION

LOG_FILE = os.path.join(BASE_DIR, 'logs/django.log')

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '\t'.join([
                '[%(levelname)s]',
                '%(asctime)s',
                'module:%(module)s',
                'process:%(process)d',
                'thread:%(thread)d',
                'message:%(message)s',
            ])
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'default',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'money': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

try:
    # pylint: disable=wildcard-import,unused-wildcard-import
    from .local_settings import *
except ImportError:
    pass

SITE_URL = f'{URL_PREFIX}/money/'
LOGIN_TARGETS = (f'{URL_PREFIX}/money/', )

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar', ]
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda request: True}
