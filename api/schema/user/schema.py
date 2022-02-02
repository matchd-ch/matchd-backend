import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_auth.settings import graphql_auth_settings
from graphql_jwt.decorators import login_required

from django.contrib.auth import get_user_model

from api.schema.profile_type import ProfileType


class User(DjangoObjectType):
    type = graphene.Field(graphene.NonNull(ProfileType))

    class Meta:
        model = get_user_model()
        interfaces = (relay.Node, )
        filter_fields = graphql_auth_settings.USER_NODE_FILTER_FIELDS
        exclude = graphql_auth_settings.USER_NODE_EXCLUDE_FIELDS.append('id')
        skip_registry = True
        convert_choices_to_enum = False


class UserQuery(ObjectType):
    me = graphene.Field(User)

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            user = get_user_model().objects.prefetch_related('student', 'company__users',
                                                             'company__benefits', 'company__branches').\
                select_related('company').get(pk=user.id)
            return user
        return None
