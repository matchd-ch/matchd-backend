import graphene
import graphql_jwt


# pylint: disable=R0903
from graphql_auth import mutations


class AuthMutation(graphene.ObjectType):
    token_auth = mutations.ObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class LogoutMutation(graphene.Mutation):
    logout = graphene.Field(graphene.Boolean)

    def resolve_logout(self, info):
        return True

    def mutate(self, info):
        pass
