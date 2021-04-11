from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG_TOOLBAR = True  # os.getenv('DEBUG_TOOLBAR', False) == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y1m_k!q=s(7m&8!)91-#9wan_568xbvqg_8$hfl@dkhy_ep#u-'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = os.getenv('DJANGO_EMAIL_USE_SSL', False)
EMAIL_USE_TLS = os.getenv('DJANGO_EMAIL_USE_TLS', False)
BASE_URL = os.getenv('DJANGO_BASE_URL', 'http://api.matchd.lo:8080')

INSTALLED_APPS += [
    'debug_toolbar',
    'graphiql_debug_toolbar',
]

MIDDLEWARE += [
    # temporary fix. waiting for https://github.com/flavors/django-graphiql-debug-toolbar/pull/12 to be merged
    # 'graphiql_debug_toolbar.middleware.DebugToolbarMiddleware',
    'api.middleware.DebugToolbarMiddleware'
]

GRAPHIQL_ENABLED = True


# DEBUG TOOLBAR
def show_debug_toolbar(request):
    return DEBUG_TOOLBAR


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_debug_toolbar,
}


GRAPHQL_JWT.update({
    'JWT_COOKIE_SECURE': False
})


CSRF_COOKIE_DOMAIN = os.getenv('APP_CSRF_COOKIE_DOMAIN', '.matchd.lo')

try:
    from .local import *
except ImportError:
    pass
