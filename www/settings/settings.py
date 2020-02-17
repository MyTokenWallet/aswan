# coding: utf-8
import os
import environ
import importlib
# from config import BASE_DIR
from django.utils.translation import gettext_lazy as _, gettext_noop

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware,'
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'permissions.middleware.PermissionsMiddleware',
    'permissions.middleware.UserAuditMiddleware'
)
LANGUAGES = (
    ('en', gettext_noop('English')),
    ('zh', gettext_noop('Chinese')),
)

p = environ.Path(__file__) - 2
env = environ.Env()


def root(*paths, **kwargs):
    ensure = kwargs.pop('ensure', False)
    path = p(*paths, **kwargs)
    if ensure and not os.path.exists(path):
        os.makedirs(path)
    return path


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/Los_Angeles'

# LANGUAGE_CODE = 'zh-hans'
# TIME_ZONE = 'Asia/Shanghai'

PROJECT_DIR = root()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qv%**nr#*m_$$36b_20dl5&rlov^%$=!gm&(y5q-@un=y#uxvl'

ALLOWED_HOSTS = [
    "*",
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_tables2',
    'crispy_forms',

    'risk_auth',
    'permissions',
    'strategy',
    'menu',
    'rule',
    'bk_config',
    'log_manage',
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
#https://docs.djangoproject.com/en/3.0/topics/i18n/formatting/
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

for dir in [parent_dir, PROJECT_DIR]:
    if dir not in sys.path:
        sys.path = sys.path + [dir]

from log.logger import logging_config as LOGGING  # noqa

risk_env = os.environ.get('RISK_ENV', 'develop')

# If the profile does not exist, it cannot be started directly
try:
    importlib.import_module('.' + risk_env, 'settings.local_settings')
    exec('from .local_settings.{risk_env} import *'.format(risk_env=risk_env))
except Exception:
    raise AssertionError(
        _('The project should set correct RISK_ENV environment var.'))
