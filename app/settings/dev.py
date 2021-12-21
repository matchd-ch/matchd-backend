from .base import *

GRAPHQL_JWT.update({
    'JWT_COOKIE_SECURE': False
})

try:
    from .local import *
except ImportError:
    pass
