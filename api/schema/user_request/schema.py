import graphene
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from db.models import UserRequest as UserRequestModel


class UserRequestInput(graphene.InputObjectType):
    name = graphene.String(description=_('Name'))
    email = graphene.String(description=_('E-Mail'))
    message = graphene.String(description=_('Message'))


# pylint: disable=R0903
class UserRequest(graphene.Mutation):

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        input = UserRequestInput(description=_('UserRequest is required.'), required=True)

    class Meta:
        description = _('Creates a new user user request')

    @classmethod
    def mutate(cls, root, info, **form_data):
        try:
            user_request = UserRequestModel(**form_data.get('input'))
            user_request.full_clean()
            user_request.save()
        except ValidationError as error:
            return UserRequest(success=False, errors=error.messages)
        return UserRequest(success=True, errors=[])


class UserRequestMutation(graphene.ObjectType):
    user_request = UserRequest.Field()
