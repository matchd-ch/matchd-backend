import graphene
from django.contrib.auth import get_user_model
from graphql_auth.schema import UserNode
from graphql_auth.settings import graphql_auth_settings
from graphql_jwt.decorators import login_required

# pylint: disable=R0903
# pylint: disable=R0201


class UserWithProfileNode(UserNode):

    class Meta:
        model = get_user_model()
        filter_fields = graphql_auth_settings.USER_NODE_FILTER_FIELDS
        exclude = graphql_auth_settings.USER_NODE_EXCLUDE_FIELDS
        interfaces = (graphene.relay.Node,)
        skip_registry = True


class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserWithProfileNode)

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None
