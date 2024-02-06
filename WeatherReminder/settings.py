"""
Django settings for WeatherReminder project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
#import io
from datetime import timedelta

from pathlib import Path
#from dotenv import load_dotenv
#from urllib.parse import urlparse
#from google.cloud import secretmanager
#import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#load_dotenv(BASE_DIR / '.env')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(' ')

SECURE_SSL_REDIRECT = \
    os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DBNAME'),
        'HOST': os.environ.get('DBHOST'),
        'USER': os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASS'),
        'OPTIONS': {'sslmode': 'require'},
    }
}
# env = environ.Env(DEBUG=(bool, False))
# env_file = os.path.join(BASE_DIR, '.env')
#
# if os.path.isfile(env_file):
#     # read a local .env file
#     env.read_env(env_file)
# elif os.environ.get('GOOGLE_CLOUD_PROJECT', None):
#     # pull .env file from Secret Manager
#     project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
#
#     client = secretmanager.SecretManagerServiceClient()
#     settings_name = os.environ.get('SETTINGS_NAME', 'django_settings')
#     name = f'projects/{project_id}/secrets/{settings_name}/versions/latest'
#     payload = client.access_secret_version(name=name).payload.data.decode('UTF-8')
#
#     env.read_env(io.StringIO(payload))
# else:
#     raise Exception('No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('SECRET_KEY')
#
# # SECURITY WARNING: don't run with debug turned on in production!
# #DEBUG = env('DEBUG')
# DEBUG = False

# ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS settings
#
# APPENGINE_URL = env('APPENGINE_URL', default=None)
# if APPENGINE_URL:
#     # ensure a scheme is present in the URL before it's processed.
#     if not urlparse(APPENGINE_URL).scheme:
#         APPENGINE_URL = f'https://{APPENGINE_URL}'
#
#     ALLOWED_HOSTS = [urlparse(APPENGINE_URL).netloc]
#     CSRF_TRUSTED_ORIGINS = [APPENGINE_URL]
#     SECURE_SSL_REDIRECT = True
# else:
#     ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'subscription',
    'getweather',
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

ROOT_URLCONF = 'WeatherReminder.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'WeatherReminder.wsgi.application'


# Database setting for local development
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Database
# [START db_setup]
# [START gaestd_py_django_database_config]
# Use django-environ to parse the connection string
# DATABASES = {"default": env.db()}
# # # If the flag as been set, configure to use proxy
# if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
#     DATABASES["default"]["HOST"] = "127.0.0.1"
#     DATABASES["default"]["PORT"] = 5432

# [END gaestd_py_django_database_config]
# [END db_setup]

# Use a in-memory sqlite3 database when testing in CI systems
# TODO(glasnt) CHECK IF THIS IS REQUIRED because we're setting a val above
# if os.getenv("TRAMPOLINE_CI", None):
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#         }
#     }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_ROOT = BASE_DIR / 'static'
# STATIC_URL = "static/"
# STATICFILES_DIRS = []

DEFAULT_FILE_STORAGE = 'WeatherReminder.azure_storage.AzureMediaStorage'
STATICFILES_STORAGE = 'WeatherReminder.azure_storage.AzureStaticStorage'

AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_FROM = os.environ.get('WEATHER_EMAIL_FROM')
# EMAIL_HOST_USER = os.environ.get('WEATHER_EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('WEATHER_EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True