try:
    from .base import *
except ImportError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'test-key'
BASE_URL = os.getenv('DJANGO_BASE_URL', 'http://api.matchd.lo:8080')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

WAGTAILSEARCH_BACKENDS.get('default')['INDEX'] = 'test'

EMAIL_SUBJECT_PREFIX = '[TEST] '
USER_REQUEST_FORM_RECIPIENTS = [
    recipient.strip() for recipient in 'recipient1@matchd.ch, recipient2@matchd.ch'.split(',')
]
