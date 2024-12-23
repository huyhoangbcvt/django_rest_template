"""
Django settings for django_rest_template project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

import os
from os.path import join
from datetime import timedelta
from Tools.scripts.win_add2path import DEFAULT
from django.core.wsgi import get_wsgi_application

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
USE_L10N = False
DATE_INPUT_FORMATS = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1lf$6zr&q&y0hgw+7kn8&zg+3zn%x%-esju#q(lmexr(61qd%&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',  # connect secure header: browser & server allow
    # Error: swagger drf_yasg duplicate if using djoser
    # 'djoser',                       # third party package for user registration and authentication endpoints
    'rest_framework',  # rest API implementation library for django
    'rest_framework_simplejwt',  # JWT authentication backend library
    # 'storages',  #S3-AWS
    'rest_framework.authtoken',  # TokenAuthentication

    'django.contrib.humanize',
    # Format number: 4500000 becomes 4,500,000 | 4500.2 becomes 4,500.2 | 450000 becomes '450.000'
    'user_app',  # modules 1
    'catalog_app',  # modules 2
    'upload_app',
    'debug_toolbar',
    'ckeditor',
    'ckeditor_uploader',
    'drf_yasg',
    'oauth2_provider',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # load file in static
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Only using when debug=True
]

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    'dev.hd.com.vn',
    # ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # Tạo JWT và xác thực quyền truy cập
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # ACCESS_TOKEN_LIFETIME
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',  # Basic Auth
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Need Authorization Headers
        # If not specified, this setting defaults to allowing unrestricted access:
        # 'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# CORS_ORIGIN_ALLOW_ALL = True  # False not allow
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:8083",
    "http://dev.hd.com.vn:8083",
]
# CORS_ALLOWED_METHODS = [
#     "GET", "POST", "PUT", "PATCH",
# ]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Expire token
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # Expire to refresh token
}

ROOT_URLCONF = 'django_rest_template.urls'

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
                'django.template.context_processors.media',  # Setup cho view {{ MEDIA_URL }}
            ],
        },
    },
]

WSGI_APPLICATION = 'django_rest_template.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_rest_template',
        'USER': 'postgres',
        'PASSWORD': 'laptrinh123456',
        'HOST': 'localhost',
        'PORT': '5433',
        'ATOMIC_REQUESTS': True,  # transactional db
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'vi'  # default language
LANGUAGES = (
    ('vi', 'Vietnamese'),
    ('en', 'English'),
    ('fr', 'French'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# =================| Handling Static files |======================
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/' #static/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WHITENOISE_USE_FINDERS = True  #important mapping, cài đặt pip install whitenoise
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# =================| Root media Configuration |======================
MEDIA_URL = "/media/"  # django.template.context_processors.media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_ROOT = '/ftp/django_rest_template/media/'

# Upload Handlers
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
]
# =======| CKEditor settings |=========
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
# This ensures you have all toolbar icons
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}
# -----------------------------------------
# CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads')
# CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
# CKEDITOR_MEDIA_PREFIX  = "/media/ckeditor/"
# CKEDITOR_UPLOAD_PREFIX = "http://fortezzeimperiali/media/uploads/"
# CKEDITOR_RESTRICT_BY_USER = True
# CKEDITOR_IMAGE_BACKEND = "pillow"

# =================| Email Configuration |=======================
# SECRET_KEY = os.environ.get('', '')
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

DEFAULT_FROM_EMAIL = 'no_reply@'
SERVER_EMAIL = 'no_reply@'
ADMINS = [('', SERVER_EMAIL), ]
MANAGERS = ADMINS
EMAIL_HOST = ''  # 'smtp.gmail.com' #MAIL_SERVER
EMAIL_HOST_USER = SERVER_EMAIL
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============= Logging Configuration ============
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',  # join(BASE_DIR, 'my_logs', 'debug.log'),
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

try:
    from django_rest_template.local_settings import *
except ImportError:
    pass
