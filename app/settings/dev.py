from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y1m_k!q=s(7m&8!)91-#9wan_568xbvqg_8$hfl@dkhy_ep#u-'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = os.getenv('DJANGO_EMAIL_USE_SSL', False)
EMAIL_USE_TLS = os.getenv('DJANGO_EMAIL_USE_TLS', False)
BASE_URL = os.getenv('DJANGO_BASE_URL', 'http://api.matchd.lo:8080')

try:
    from .local import *
except ImportError:
    pass
