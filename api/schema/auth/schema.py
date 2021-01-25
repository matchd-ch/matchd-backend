import graphene
import graphql_jwt

from graphql_auth import mutations


class AuthMutation(graphene.ObjectType):
    token_auth = mutations.ObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = graphql_jwt.Revoke.Field()
