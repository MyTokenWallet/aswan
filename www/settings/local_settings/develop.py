# coding=utf8
"""Development environment configuration"""

DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.mysql',
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": "root",
        "DATABASE_CHARSET": "utf8",
        "NAME": "risk_control",
    },
}

DEBUG = True
