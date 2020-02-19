# coding: utf-8

from django.utils.translation import gettext as _
import environ
import importlib


# from django.utils.crypto import get_random_string

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wb_*$8@jq=rl@dlx207h+l6k=p+ti@w(i9p^p-lozgp8(9wws-'

#chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
#SECRET_KEY = get_random_string(50, chars)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "")

ALLOWED_HOSTS = []

SILENCED_SYSTEM_CHECKS = [
    'admin.E408',
    'admin.E409',
    'admin.E410',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'permissions.middleware.PermissionsMiddleware',
    'permissions.middleware.UserAuditMiddleware',
    'django.middleware.locale.LocaleMiddleware,'
]

LANGUAGES = (
    ('en', _('English')),
    ('zh', _('Chinese')),
)

p = environ.Path(__file__) - 2
env = environ.Env()


def root(*paths, **kwargs):
    ensure = kwargs.pop('ensure', False)
    path = p(*paths, **kwargs)
    if ensure and not os.path.exists(path):
        os.makedirs(path)
    return path

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR + "www", 'locale'),
)

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'

# LANGUAGE_CODE = 'zh-hans'
# TIME_ZONE = 'Asia/Shanghai'

PROJECT_DIR = root()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


ALLOWED_HOSTS = [
    "*",
]

# Application definition

INSTALLED_APPS = (
    'www',
    'bk_config',
    'core',
    'log_manage',
    'menu',
    'permissions',
    'risk_auth',
    'rule',
    'settings',
    'strategy',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'crispy_forms',
)

# https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#how-django-discovers-language-preference


ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'permissions.context_processors.menu_by_perms',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

USE_I18N = True
USE_L10N = True
USE_TZ = True
# https://docs.djangoproject.com/en/3.0/topics/i18n/formatting/
USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = root('media')

STATIC_ROOT = root('site-static')

STATICFILES_DIRS = (root('static'),)

# Policy signature key
STRATEGY_SIGN_KEY = 'strategy_sign'

# Save the latest rule ID for generation
LAST_RULE_ID_KEY = 'last_rule_id'

import sys  # noqa

parent_dir = os.path.abspath(os.path.join(PROJECT_DIR, "../"))

for my_dir in [parent_dir, PROJECT_DIR]:
    if my_dir not in sys.path:
        sys.path = sys.path + [my_dir]

# from log.logger import logging_config as LOGGING  # noqa

risk_env = os.environ.get('RISK_ENV', 'develop')

# If the profile does not exist, it cannot be started directly
try:
    importlib.import_module('.' + risk_env, 'settings.local_settings')
    exec('from .local_settings.{risk_env} import *'.format(risk_env=risk_env))
except Exception:
    raise AssertionError(
        _('The project should set correct RISK_ENV environment var.'))
