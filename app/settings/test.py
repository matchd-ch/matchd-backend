try:
    from .base import *
except ImportError:
    pass

SECRET_KEY = 'test-key'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

WAGTAILSEARCH_BACKENDS.get('default')['INDEX'] = 'test'

EMAIL_SUBJECT_PREFIX = '[TEST] '
USER_REQUEST_FORM_RECIPIENTS = [
    recipient.strip() for recipient in 'recipient1@matchd.ch, recipient2@matchd.ch'.split(',')
]

DATA_PROTECTION_URL = os.getenv('DATA_PROTECTION_URL', 'app.matchd.localhost/datenschutz')

GRAPHQL_AUTH['EMAIL_TEMPLATE_VARIABLES']['email_subject_prefix'] = EMAIL_SUBJECT_PREFIX
GRAPHQL_AUTH['EMAIL_TEMPLATE_VARIABLES']['data_protection_url'] = DATA_PROTECTION_URL
GRAPHQL_AUTH['EMAIL_SUBJECT_ACTIVATION'] = 'db/tests/email/activation/subject.txt'
GRAPHQL_AUTH['EMAIL_TEMPLATE_ACTIVATION'] = 'db/tests/email/activation/body.html'
GRAPHQL_AUTH['EMAIL_SUBJECT_PASSWORD_RESET'] = 'db/tests/email/password_reset/subject.txt'
GRAPHQL_AUTH['EMAIL_TEMPLATE_PASSWORD_RESET'] = 'db/tests/email/password_reset/body.html'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_test')
MEDIA_FIXTURE_ROOT = os.path.join(BASE_DIR, 'media_fixtures')
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
