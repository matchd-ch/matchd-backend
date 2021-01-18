from .base import *

DEBUG = False
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'unix_socket': '/var/run/mysqld/mysqld.sock',
        },
        'NAME': os.getenv('DJANGO_DB_NAME', ''),
        'USER': os.getenv('DJANGO_DB_USER', ''),
        'PASSWORD': os.getenv('DJANGO_DB_PW', '')
    }
}

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
