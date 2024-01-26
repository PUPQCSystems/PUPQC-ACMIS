"""
Django settings for ACIS_system_v1 project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os

import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3u_ik-u)s!pe@ccyhjhvg%^zk&gozhm6z^$c4(z4adm07ue)on'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CRISPY_FAIL_SILENTLY = not DEBUG

# I added '*' to the allowed so that it can allow ALL host
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'whitenoise',
    'django.contrib.staticfiles',

    'rest_framework',
    "corsheaders",

    # 'debug_toolbar',
    'fontawesomefree',
    "crispy_forms",
    "crispy_bootstrap5",

    'Programs',
    'Users.apps.UsersConfig',
    'Dashboard',
    'Accreditation',
    'LandingPage',
    'Api',


]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
 
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


ROOT_URLCONF = 'ACIS_system_v1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ACIS_system_v1.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),

}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         'NAME': 'ACIS-Database',
#         'USER': 'ACIS',
#         'PASSWORD': 'acis' ,
#         "HOST": "127.0.0.1",
#         "PORT": "5432",
#     }
# }


# Database settings for render deployment
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://acis_database_user:pxH4rLwHUXeUbSurrnwzo1iVjpU41MiK@dpg-cmp1oj6g1b2c73f83co0-a.singapore-postgres.render.com/acis_database',
    )
}


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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]

MEDIA_URL = '/file-storage/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'file-storage')
# STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')


#Edited for deployment
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'ACIS_system_v1/static']


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'  

AUTH_USER_MODEL = 'Users.CustomUser'
