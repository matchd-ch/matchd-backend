from .base import *

DEBUG = False
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

try:
    from .local import *
except ImportError:
    pass
