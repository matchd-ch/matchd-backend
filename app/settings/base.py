"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'wagtailfontawesome',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',

    'graphene_django',
    'corsheaders',
    'graphql_auth',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'db.apps.DbConfig',
    'api.apps.ApiConfig'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'graphql_auth.backends.GraphQLAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]


ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'charset': 'utf8mb4'},
        'NAME': os.getenv('DJANGO_DB_NAME', ''),
        'USER': os.getenv('DJANGO_DB_USER', ''),
        'PASSWORD': os.getenv('DJANGO_DB_PW', ''),
        'HOST': os.getenv('DJANGO_DB_HOST', ''),
        'PORT': os.getenv('DJANGO_DB_PORT', ''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'db.validators.PasswordValidator'
    }
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# E-Mail Settings
DEFAULT_FROM_EMAIL = os.getenv('DJANGO_EMAIL', '')
EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST', '')
EMAIL_PORT = os.getenv('DJANGO_EMAIL_PORT', '')
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER', '')
EMAIL_USE_SSL = os.getenv('DJANGO_EMAIL_USE_SSL', True)
EMAIL_USE_TLS = os.getenv('DJANGO_EMAIL_USE_TLS', False)
EMAIL_SUBJECT_PREFIX = os.getenv('DJANGO_EMAIL_SUBJECT_PREFIX', '')
USER_REQUEST_FORM_RECIPIENTS = [
    recipient.strip() for recipient in os.getenv('USER_REQUEST_FORM_RECIPIENTS', f'{DEFAULT_FROM_EMAIL}').split(',')
]

# FRONTEND
FRONTEND_URL = os.getenv('FRONTEND_URL', '')


# Wagtail settings

WAGTAIL_SITE_NAME = "Matchd"

# Prefix Index to allow for ressource sharing
INDEX_PREFIX = os.getenv('DJANGO_ELASTIC_INDEX_PREFIX', 'local').replace('-', '_')

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch7',
        'URLS': [os.getenv('DJANGO_ELASTIC_SEARCH_URL', '')],
        'INDEX': f'{INDEX_PREFIX}_matchd',
        'TIMEOUT': 5,
        'OPTIONS': {},
        'INDEX_SETTINGS': {}
    }
}


# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = os.getenv('DJANGO_BASE_URL', '')

APP_DOMAIN = os.getenv('APP_DOMAIN')

AUTH_USER_MODEL = 'db.User'

GRAPHIQL_ENABLED = os.getenv('DJANGO_GRAPHIQL_ENABLED', False)

# Graphene Settings
GRAPHENE = {
    'SCHEMA': 'api.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ]
}

# CORS
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^http(s?)://localhost(:?)\d{0,5}$",
    r"^http(s?)://(.*\.)?matchd\.lo(:\d{0,5})?$",
]

CORS_ALLOW_CREDENTIALS = True

GRAPHQL_JWT = {
    'JWT_EXPIRATION_DELTA': timedelta(hours=24),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_COOKIE_SECURE': True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.ObtainJSONWebToken",
    ],
}

GRAPHQL_AUTH = {
    'ALLOW_LOGIN_NOT_VERIFIED': False,
    'ALLOW_LOGIN_WITH_SECONDARY_EMAIL': False,
    'ALLOW_DELETE_ACCOUNT': True,
    'EXPIRATION_ACTIVATION_TOKEN': timedelta(days=7),
    'EXPIRATION_PASSWORD_RESET_TOKEN': timedelta(hours=1),
    'EMAIL_FROM': DEFAULT_FROM_EMAIL,
    'ACTIVATION_PATH_ON_EMAIL': 'aktivierung',
    'PASSWORD_RESET_PATH_ON_EMAIL': 'password-reset',
    'EMAIL_SUBJECT_ACTIVATION': 'api/email/activation/subject.txt',
    'EMAIL_TEMPLATE_ACTIVATION': 'api/email/activation/body.html',
    'EMAIL_SUBJECT_PASSWORD_RESET': 'api/email/password_reset/subject.txt',
    'EMAIL_TEMPLATE_PASSWORD_RESET': 'api/email/password_reset/body.html',
    'EMAIL_TEMPLATE_VARIABLES': {
        'frontend_url': FRONTEND_URL,
        'email_subject_prefix': EMAIL_SUBJECT_PREFIX
    },
    'USER_NODE_EXCLUDE_FIELDS': ['password', 'is_superuser', 'is_staff', 'last_login', 'is_active', 'date_joined'],
    'REGISTER_MUTATION_FIELDS': ['email', 'username', 'first_name', 'last_name'],
    'REGISTER_MUTATION_FIELDS_OPTIONAL': ['type']
}

CSRF_COOKIE_DOMAIN = os.getenv('APP_CSRF_COOKIE_DOMAIN', None)
