import graphene
import graphql_jwt

# pylint: disable=R0903
from django.contrib.auth import get_user_model
from graphene import String
from graphql_auth import mutations
from graphql_auth.constants import TokenAction
from graphql_auth.settings import graphql_auth_settings
from graphql_auth.utils import get_token_paylod


class AuthMutation(graphene.ObjectType):
    token_auth = mutations.ObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()


# pylint: disable=R0201
# pylint: disable=W0703
class VerifyPasswordResetToken(graphene.ObjectType):
    verify_password_reset_token = graphene.Field(
        graphene.Boolean,
        token=String(required=True)
    )

    # noinspection PyBroadException
    def resolve_verify_password_reset_token(self, info, token):
        try:
            payload = get_token_paylod(
                token,
                TokenAction.PASSWORD_RESET,
                graphql_auth_settings.EXPIRATION_PASSWORD_RESET_TOKEN
            )
            return get_user_model().objects.filter(username=payload.get('username', None)).exists()
        except Exception:
            return False
