"""
Django settings for ControlPanel project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
CP2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # ControlPanel
IPOLDEVEL_DIR = os.path.normpath(os.path.join(CP2_DIR, '../..')) # ipolDevel
HOME_DIR = os.path.normpath(os.path.join(IPOLDEVEL_DIR, '..')) # ipol user folder



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ng&u0bv6bm6cs+w+c#=*b0-#g-e_*t(my7(q@&1@^b5m@-)&^!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HOST_NAME = os.environ.get('IPOL_HOST', socket.getfqdn())
IPOL_URL = os.environ.get('IPOL_URL', 'http://' + socket.getfqdn())
ALLOWED_HOSTS = []

ACCOUNT_EMAIL_VERIFICATION = 'none'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
if HOST_NAME in ['127.0.0.1', 'localhost']:
    # Mails shown on the terminal output
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Use system default mailing config
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

dev_machines = ['127.0.0.1', 'localhost', 'integration.ipol.im']
production_servers = ['ipolcore.ipol.im']

ALLOWED_HOSTS = [HOST_NAME]

CORS_ALLOWED_ORIGINS = [
    IPOL_URL,
    'localhost',
    '127.0.0.1'
]
CSRF_TRUSTED_ORIGINS = [
    IPOL_URL,
    'http://localhost',
    'http://127.0.0.1'
]

if HOST_NAME in dev_machines:
    ALLOWED_HOSTS = [HOST_NAME, '127.0.0.1', 'localhost']
    DEBUG = True
elif HOST_NAME in production_servers:
    DEBUG = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
# python3 manage.py collectstatic pour copier les fichiers static (du projet et de l'admin) dans 
STATIC_URL = 'cp2/static/'
STATIC_ROOT = os.path.join(HOME_DIR, 'CP2_STATIC')
STATICFILES_DIRS = (
#     # Put strings here, like "/home/html/static" or "C:/www/django/static".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
    os.path.join(CP2_DIR, 'static_cp'),
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ControlPanel',
    'gunicorn',
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

ROOT_URLCONF = 'ControlPanel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(CP2_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'ControlPanel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(CP2_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}