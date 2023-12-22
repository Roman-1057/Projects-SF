import os
import json
import sys
import loguru
import logging
from django.conf import settings

from dotenv import load_dotenv
from pathlib import Path

from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-&(k-*uckawq#85bup%cv-3fam@xx_#^*$6ij(qo26+9)_#rb+8'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

SITE_ID = 1

INSTALLED_APPS = [
    'news.apps.NewsConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',
]

MIDDLEWARE = [
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'News_Portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'News_Portal.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/news'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_CONFIRMATION_SIGNUP_MESSAGE = "account/email/email_confirmation_signup_message.html"
ACCOUNT_FORMS = {'signup': 'news.forms.BasicSignupForm'}

load_dotenv()

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

SITE_URL = 'http://127.0.0.1:8000'

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
broker_connection_retry_on_startup = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        'TIMEOUT': 30,
    }
}

# Регистрируем основной логгер Django
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter',
        },
        'general_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/general.log',
            'formatter': 'file_formatter',
        },
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'formatter': 'errors_formatter',
        },
        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'file_formatter',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False,
            'filters': ['request_filter'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'general_file', 'errors_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'filters': {
        'request_filter': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: not settings.DEBUG,
        },
    },
    'formatters': {
        'console_formatter': {
            'format': '{asctime} [{levelname}] {message}',
            'style': '{',
            'datefmt': '%d.%m.%Y %H:%M:%S',
        },
        'file_formatter': {
            'format': '{asctime} [{levelname}] {module} {message}',
            'style': '{',
            'datefmt': '%d.%m.%Y %H:%M:%S',
        },
        'errors_formatter': {
            'format': '{asctime} [{levelname}] {message}\n{pathname}\n{exc_info}',
            'style': '{',
            'datefmt': '%d.%m.%Y %H:%M:%S',
        },
        'pathname': {
            'format': '[%(asctime)s] %(levelname)s %(pathname)s %(message)s',
            'datefmt': '%d.%m.%Y %H:%M:%S',
        },
        'exc_info': {
            'format': '[%(asctime)s] %(levelname)s %(pathname)s %(message)s\n%(exc_info)s',
            'datefmt': '%d.%m.%Y %H:%M:%S',
        },
    },
}


logger = logging.getLogger('django')

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message', exc_info=True)
logger.critical('Critical message', exc_info=True)

loguru.logger.add(sys.stdout, level="DEBUG",
                  format="<green>{time:DD.MM.YYYY HH:mm:ss}</green> | <level>{level: <8}</level> | "
                         "<cyan>{message}</cyan>")


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
   ('ru', _('Russian')),
   ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

