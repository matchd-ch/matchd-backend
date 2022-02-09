import graphene
from graphene import ObjectType
from graphql_auth.bases import Output

from django.utils.translation import gettext_lazy as _

from db.forms import UserRequestForm
from db.models import UserRequest as UserRequestModel


class UserRequestInput(graphene.InputObjectType):
    name = graphene.String(description=_('Name'), required=True)
    email = graphene.String(description=_('E-Mail'), required=True)
    message = graphene.String(description=_('Message'), required=True)


class UserRequest(Output, graphene.Mutation):

    class Arguments:
        input = UserRequestInput(description=_('UserRequest is required.'), required=True)

    class Meta:
        description = _('Creates a new user user request')

    @classmethod
    def mutate(cls, root, info, **form_data):
        errors = {}
        user_request_data = form_data.pop('input')
        user_request = None

        user_request_form = UserRequestForm(user_request_data)
        user_request_form.full_clean()

        if user_request_form.is_valid():
            user_request = UserRequestModel(**user_request_data)
            user_request.save()
        else:
            errors.update(user_request_form.errors.get_json_data())

        return UserRequest(success=not errors, errors=errors)


class UserRequestMutation(ObjectType):
    user_request = UserRequest.Field()
