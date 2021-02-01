import graphene

from api.schema.auth import AuthMutation, LogoutMutation
from api.schema.registration import RegistrationMutation
from api.schema.user import UserQuery
from api.schema.user_request import UserRequestMutation


class Mutation(
    RegistrationMutation,
    UserRequestMutation,
    AuthMutation,
    LogoutMutation
):
    pass


class Query(UserQuery):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
