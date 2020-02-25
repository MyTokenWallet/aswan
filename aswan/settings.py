# coding: utf-8
import importlib
import os
import sys
import environ
from dotenv import load_dotenv
from pathlib import Path  # python3 only

# from django.utils.crypto import get_random_string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wb_*$8@jq=rl@dlx207h+l6k=p+ti@w(i9p^p-lozgp8(9wws-'

# chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
# SECRET_KEY = get_random_string(50, chars)

CRISPY_TEMPLATE_PACK = 'bootstrap'  # uni_form or bootstrap
CSRF_TRUSTED_ORIGINS = ['127.0.0.1', 'localhost', ]
DATABASE_ROUTERS = []
DEFAULT_FROM_EMAIL = ['michael.padilla@zwilla.de']
ALLOWED_HOSTS = [
    '*',
    '127.0.0.1',
    'localhost',
    '[::1]',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.staticfiles.finders',
    'django_tables2',
    'django.views.i18n',
    'crispy_forms',

    'aswan',
    'aswan.local_settings',
    'aswan.risk_auth',
    'aswan.permissions',
    'aswan.strategy',
    'aswan.menu',
    'aswan.rule',
    'aswan.bk_config',
    'aswan.log_manage',

]

SILENCED_SYSTEM_CHECKS = [
    'admin.E408',
    'admin.E409',
    'admin.E410',
    'models.E028',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'aswan.permissions.middleware.PermissionsMiddleware',
    'aswan.permissions.middleware.UserAuditMiddleware',
]

ADMINS = [('zwilla', 'info@zwilla.de')]

LANGUAGES = (
    ('en', 'English'),
    ('zh', 'Chinese'),
)


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

# Policy signature key
STRATEGY_SIGN_KEY = 'strategy_sign'

# Save the latest rule ID for generation
LAST_RULE_ID_KEY = 'last_rule_id'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SITE_ROOT = os.path.dirname(os.path.realpath(__name__))

LOCALE_PATHS = (
    os.path.join(SITE_ROOT + "/", 'locale'),
    #    os.path.join(SITE_ROOT + "/aswan/riksy_auth", 'locale'),
    #    os.path.join(SITE_ROOT, 'locale'),
)
LOGOUT_REDIRECT_URL = ['/']
MANAGERS = ['zwilla']
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'

# LANGUAGE_CODE = 'zh-hans'
# TIME_ZONE = 'Asia/Shanghai'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#how-django-discovers-language-preference
ROOT_URLCONF = 'aswan.urls'

WSGI_APPLICATION = 'aswan.wsgi.application'

USE_I18N = True
USE_L10N = True
USE_TZ = True
# https://docs.djangoproject.com/en/3.0/topics/i18n/formatting/
USE_THOUSAND_SEPARATOR = True

p = environ.Path(__file__) - 2
env = environ.Env()


def root(*paths, **kwargs):
    ensure = kwargs.pop('ensure', False)
    path = p(*paths, **kwargs)
    if ensure and not os.path.exists(path):
        os.makedirs(path)
    return path


PROJECT_DIR = root()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'aswan/templates'),
            os.path.join(BASE_DIR, 'aswan/risk_auth/templates/risk_auth'),
            os.path.join(BASE_DIR, 'aswan/log_manage/templates/log_manage'),
            os.path.join(BASE_DIR, 'aswan/rule/templates/rule'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'aswan.permissions.context_processors.menu_by_perms',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# STATIC_URL = ''
MEDIA_URL = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MEDIA_ROOT = root('media')
STATIC_ROOT = root('site-static')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

parent_dir = os.path.abspath(os.path.join(PROJECT_DIR, "../"))

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

override = True

for my_dir in [parent_dir, PROJECT_DIR]:
    if my_dir not in sys.path:
        sys.path = sys.path + [my_dir]

os.environ.setdefault('RISK_ENV', 'develop')
# risk_env = ['RISK_ENV', 'develop']
# risk_env = 'develop'
risk_env = os.environ.get('RISK_ENV', 'develop')
# If the profile does not exist, it cannot be started directly
try:
    importlib.import_module('.' + risk_env, 'aswan.local_settings')
    exec('from aswan.local_settings.{risk_env} import *'.format(risk_env=risk_env))
except Exception:
    raise AssertionError(
        'The project should set correct RISK_ENV environment var.')
