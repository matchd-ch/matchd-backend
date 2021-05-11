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

GRAPHQL_AUTH['EMAIL_TEMPLATE_VARIABLES']['email_subject_prefix'] = EMAIL_SUBJECT_PREFIX

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_test')
MEDIA_URL = '/media_test/'

MATCHING_VALUE_BRANCH = 0
MATCHING_VALUE_JOB_TYPE = 3
MATCHING_VALUE_WORKLOAD = 1
MATCHING_VALUE_CULTURAL_FITS = 3
MATCHING_VALUE_SOFT_SKILLS = 3
MATCHING_VALUE_SKILLS = 3
MATCHING_VALUE_LANGUAGES = 2
MATCHING_VALUE_DATE_OR_DATE_RANGE = 5

MATCHING_VALUE_DATE_OR_DATE_RANGE_PRECISION = [0]
MATCHING_VALUE_WORKLOAD_PRECISION = [0]

NUMBER_OF_STUDENT_AVATAR_FALLBACK_IMAGES = 2
NUMBER_OF_COMPANY_AVATAR_FALLBACK_IMAGES = 2
