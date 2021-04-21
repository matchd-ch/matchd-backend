import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_auth.settings import graphql_auth_settings
from graphql_jwt.decorators import login_required

from api.schema.profile_type import ProfileType


class User(DjangoObjectType):
    type = graphene.Field(graphene.NonNull(ProfileType))

    class Meta:
        model = get_user_model()
        filter_fields = graphql_auth_settings.USER_NODE_FILTER_FIELDS
        exclude = graphql_auth_settings.USER_NODE_EXCLUDE_FIELDS
        skip_registry = True
        convert_choices_to_enum = False


class UserQuery(graphene.ObjectType):
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
