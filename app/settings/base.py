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
from urllib.parse import urlparse

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'db.apps.DbConfig',
    'wagtailfontawesome',
    'wagtailmedia',
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
    'api.middleware.JWTAuthenticationMiddleware'
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'graphql_auth.backends.GraphQLAuthBackend',
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
EMAIL_USE_SSL = os.getenv('DJANGO_EMAIL_USE_SSL', False)
EMAIL_USE_TLS = os.getenv('DJANGO_EMAIL_USE_TLS', True)
EMAIL_SUBJECT_PREFIX = os.getenv('DJANGO_EMAIL_SUBJECT_PREFIX', '')
USER_REQUEST_FORM_RECIPIENTS = [
    recipient.strip() for recipient in os.getenv('USER_REQUEST_FORM_RECIPIENTS', f'{DEFAULT_FROM_EMAIL}').split(',')
]

# FRONTEND
FRONTEND_URL_PROTOCOL = 'https://'
FRONTEND_URL = os.getenv('FRONTEND_URL', '')

STUDENT_PROFILE_URL = '/talente/'
JOB_POSTING_URL = '/stellen/'

# DATA PROTECTION
DATA_PROTECTION_URL = os.getenv('DATA_PROTECTION_URL', '')

# Wagtail settings

WAGTAIL_SITE_NAME = os.getenv('WAGTAIL_SITE_NAME', 'MATCHD')

# Prefix Index to allow for ressource sharing
INDEX_PREFIX = os.getenv('DJANGO_ELASTIC_INDEX_PREFIX', 'local').replace('-', '_')


def get_elasticsearch_url():
    url = os.getenv('DJANGO_ELASTIC_SEARCH_URL', '')
    protocol = 'http'
    port = ''
    if url and url != '':
        parsed_uri = urlparse(url)
        protocol = parsed_uri.scheme
        url = parsed_uri.hostname
        port = parsed_uri.port
    if port and port != '':
        port = f':{port}'

    user = os.getenv('DJANGO_ELASTIC_SEARCH_USER', '')
    password = os.getenv('DJANGO_ELASTIC_SEARCH_PASSWORD', '')

    elasticsearch_url = ''
    if user and user != '' and password and password != '':
        elasticsearch_url = f'{user}:{password}@'
    return f'{protocol}://{elasticsearch_url}{url}{port}'


WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch7',
        'URLS': [get_elasticsearch_url()],
        'INDEX': f'{INDEX_PREFIX}_matchd',
        'TIMEOUT': 5,
        'OPTIONS': {},
        'INDEX_SETTINGS': {}
    }
}

WAGTAILDOCS_DOCUMENT_MODEL = 'db.File'
WAGTAILMEDIA_MEDIA_MODEL = 'db.Video'
WAGTAILIMAGES_IMAGE_MODEL = 'db.Image'

# Image Stacks
IMAGE_STACKS = {
    'company-detail-media': 'fill-1280x720',
    'company-detail-media-small': 'fill-800x450',
    'logo': 'width-240',
    'desktop': 'fill-800x600',
    'mobile': 'fill-640x480',
    'desktop-square': 'fill-400x400',
    'mobile-square': 'fill-200x200',
    'avatar': 'fill-240x240'
}

USER_UPLOADS_IMAGE_TYPES = ('image/jpeg', 'image/png', 'image/gif',)
USER_UPLOADS_MAX_IMAGE_SIZE = 1024 * 10000

USER_UPLOADS_VIDEO_TYPES = ('video/mp4',)
USER_UPLOADS_MAX_VIDEO_SIZE = 1024 * 100000

USER_UPLOADS_DOCUMENT_TYPES = ('application/pdf',)
USER_UPLOADS_MAX_DOCUMENT_SIZE = 1024 * 10000


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
    r"^http(s?)://(.*\.)?matchd\.ch(:\d{0,5})?$",
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
    'PASSWORD_RESET_PATH_ON_EMAIL': 'passwort-reset',
    'EMAIL_SUBJECT_ACTIVATION': 'db/email/activation/subject.txt',
    'EMAIL_TEMPLATE_ACTIVATION': 'db/email/activation/body.html',
    'EMAIL_SUBJECT_PASSWORD_RESET': 'db/email/password_reset/subject.txt',
    'EMAIL_TEMPLATE_PASSWORD_RESET': 'db/email/password_reset/body.html',
    'EMAIL_TEMPLATE_VARIABLES': {
        'frontend_url': FRONTEND_URL,
        'frontend_url_protocol': FRONTEND_URL_PROTOCOL,
        'email_subject_prefix': EMAIL_SUBJECT_PREFIX,
        'data_protection_url': DATA_PROTECTION_URL
    },
    'USER_NODE_EXCLUDE_FIELDS': ['password', 'is_superuser', 'is_staff', 'last_login', 'is_active', 'date_joined'],
    'REGISTER_MUTATION_FIELDS': ['email', 'username', 'first_name', 'last_name', 'type'],
}

CSRF_COOKIE_DOMAIN = os.getenv('APP_CSRF_COOKIE_DOMAIN', None)

PHONE_REGEX = r'\+[0-9]{11}$'

UID_REGEX = r'CHE-[0-9]{3}\.[0-9]{3}\.[0-9]{3}$'

ZIP_CITY_DATA_SOURCE = os.path.join(BASE_DIR, 'api', 'data', 'data.json')

MATCHING_VALUE_BRANCH = 0
MATCHING_VALUE_JOB_TYPE = 3
MATCHING_VALUE_PROJECT_TYPE = 3
MATCHING_VALUE_TOPIC = 3
MATCHING_VALUE_WORKLOAD = 1
MATCHING_VALUE_CULTURAL_FITS = 3
MATCHING_VALUE_SOFT_SKILLS = 3
MATCHING_VALUE_KEYWORDS = 3
MATCHING_VALUE_SKILLS = 3
MATCHING_VALUE_LANGUAGES = 2
MATCHING_VALUE_DATE_OR_DATE_RANGE = 5

MATCHING_VALUE_DATE_OR_DATE_RANGE_PRECISION = [0]  # , 2, 6]
MATCHING_VALUE_WORKLOAD_PRECISION = [0]  # , 10, 20]

DASHBOARD_NUM_LATEST_ENTRIES = 5

NUMBER_OF_STUDENT_AVATAR_FALLBACK_IMAGES = 5
NUMBER_OF_COMPANY_AVATAR_FALLBACK_IMAGES = 5
NUMBER_OF_PROJECT_POSTING_FALLBACK_IMAGES = 5
