"""
Django settings for rapback project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print BASE_DIR

ADMINS = (
    ('Michael Paris', 'mlparis92@gmail.com'),
)

MANAGERS = ADMINS
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y$91n3x&5_lyk708h1#&!@h7-o8w_r5-*anpob#9dcg6-0m&+w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Environment specific settings
INSTANCE_ID = 'rapchat.base'
#Try to get an i nstance id from the environment
if os.environ.get('INSTANCE_ID', None):
    INSTANCE_ID = os.environ.get('INSTANCE_ID', INSTANCE_ID)
else:
    print 'WARNING: The environment variable INSTANCE_ID is not set!'
    print 'Using default settings...'

if INSTANCE_ID == 'LOCAL_VAGRANT':
    from .conf.settings_vagrant import *
elif INSTANCE_ID == 'PROD':
    from .conf.settings_prod import *

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'feedly',
    'django_extensions',
    'gunicorn',
    'djcelery',
    'api.users',
    'api.rapsessions',
    'api.feedback',
    'api.core'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rapback.urls'

WSGI_APPLICATION = 'rapback.wsgi.application'

# Shared Settings

AUTH_USER_MODEL = 'users.Profile'

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'PAGINATE_BY': 1,
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": [],
    "api_version": '0.2',
    "api_key": '',
    "enabled_methods": [
        'get',
        'post',
        'put',
    ]
}

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/ubuntu/static/'