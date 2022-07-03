import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_auth.settings import graphql_auth_settings
from graphql_jwt.decorators import login_required

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from api.schema.profile_type import ProfileType

from db.exceptions import FormException
from db.forms.user import update_user_info

# pylint: disable=W0221


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


class UpdateUserMutation(Output, relay.ClientIDMutation):
    user = graphene.Field(User)

    class Input:
        email = graphene.String(required=False)

    class Meta:
        description = _('Updates user information')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        user_data = data.get('input', None)

        try:
            updated_user = update_user_info(user, user_data)
            if not updated_user.status.verified:
                user.status.resend_activation_email(info)
        except FormException as exception:
            return UpdateUserMutation(success=False, errors=exception.errors, user=None)
        return UpdateUserMutation(success=True, errors=None, user=updated_user)


class UserMutation(graphene.ObjectType):
    update_user = UpdateUserMutation.Field()
