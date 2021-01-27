import graphene
import graphql_jwt


# pylint: disable=R0903
from graphql_auth import mutations


class AuthMutation(graphene.ObjectType):
    token_auth = mutations.ObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
