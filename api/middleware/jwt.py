from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.shortcuts import get_user_by_token
from graphql_jwt.utils import get_credentials


# custom middleware to add the user to the request
# this is required for non graphql views (eg. api.views.AttachmentServeView)
class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request, **kwargs):
        user = get_user(request)
        if user.is_authenticated:
            return user
        token = get_credentials(request, **kwargs)
        try:
            if token is not None:
                return get_user_by_token(token, request)
        except JSONWebTokenError:
            pass
        return user
