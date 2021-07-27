"""
Django settings for ProductImporter project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import datetime

import environ

env = environ.Env()
from kombu import Exchange, Queue  # celery dependencies

# Celery
CELERY_ENABLE_UTC = True
timezone = "UTC"

ALLOWED_HOSTS = ['*']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9k5uta$-g9(=xucme5gagynhui@@b0b4n!fiug5p&xg=pouc*7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ROOT_DIR = environ.Path(__file__) - 3

SITE_ROOT = os.path.dirname(os.path.realpath(__name__))
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'



# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_fsm',
    'fsm_admin',
]

LOCAL_APPS = [
    'ProductImporter.user',
    'ProductImporter.product',
]

THIRD_PARTY_APPS = [
    'django_celery_results',  # celery backend results -- redis
    'django_celery_beat',  # database backed periodic tasks

]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProductImporter.urls'

# LOGIN_URL = '/login/'
# LOGOUT_URL = 'logout'
# LOGIN_REDIRECT_URL = '/'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # 'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProductImporter.wsgi.application'
# APPS_DIR = ROOT_DIR
APPS_DIR = ROOT_DIR.path('ProductImporter')


MEDIA_ROOT = str(APPS_DIR('uploads'))

MEDIA_URL = '/media/uploads/'

AUTHENTICATION_BACKENDS = [
    #'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }



# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///blowhorn')
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['NAME'] = 'product'
# specify Postgis backend
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
DATABASES['default']['HOST'] = 'postgres'
DATABASES['default']['USER'] = 'product'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Celery
CELERY_ENABLE_UTC = True
timezone = "UTC"
from config.settings.celery import *
# configure queues, currently we have only one
task_default_queue = 'high'
task_default_exchange = 'high'
task_default_routing_key = 'high'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 4,
    'interval_start': 0,
    'interval_step': 0.5,
    'interval_max': 3,
}
CELERY_TASK_ROUTES = {
    'ProductImporter.user.tasks.send_sms': {'queue': 'high'},
}
ACTIVE_COUNTRY_CODE = '+91'


# Sensible settings for celery
task_always_eager = False
task_acks_late = True
task_publish_retry = True
worker_disable_rate_limits = False

# By default we will ignore result
# If you want to see results and try out tasks interactively,
# change it to False
# Or change this setting on tasks level
task_ignore_result = False # change
CELERY_SEND_TASK_ERROR_EMAILS = False
result_expires = 600
CELERY_EVENT_MAX_RETRIES = 3



# Set redis as celery result backend

REDIS_PORT = 6379
REDIS_DB = 0
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'redis')

result_backend = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)
redis_max_connections = 1

# Don't use pickle as serializer, json is much safer
task_serializer = "json"
accept_content = ['application/json']

worker_hijack_root_logger = False
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1000

# Celery Beat
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# RaabitMQ configs
RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'rabbit')
MEDIA_UPLOAD_STRUCTURE = "uploads/documents/{module_name}/{instance_handle}/{doc_code}/{file_name}"


if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

broker_url = os.environ.get('CELERY_BROKER_URL', '')
if not broker_url:
    broker_url = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.environ.get('RABBIT_ENV_USER', 'admin'),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'mypass'),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))

# We don't want to have dead connections stored on rabbitmq, so we have to
# negotiate using heartbeats
CELERY_BROKER_HEARTBEAT = 30
if not broker_url.endswith("?heartbeat=" + str(CELERY_BROKER_HEARTBEAT)):
    broker_url += "?heartbeat=" + str(CELERY_BROKER_HEARTBEAT)

CELERY_BROKER_POOL_LIMIT = 1
CELERY_BROKER_CONNECTION_TIMEOUT = 10
CELERY_RESULT_PERSISTENT=False

from config.settings.celery import *


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# For Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'ProductImporter.common.middleware.JSONWebTokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7)
}

EXOTEL_MASKING = 'https://%s:%s@api.exotel.com/v1/Accounts/%s/Calls/connect.json'
EXOTEL_API_SID = ''
SMS_CALLBACK_URL = ''
EXOTEL_API_TOKEN = ''